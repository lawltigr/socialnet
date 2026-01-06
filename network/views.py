from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Post, Comment, Profile, Message, Notification, SavedPost
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from .forms import EditProfileForm
from django.contrib.auth.models import User

@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    post_form = PostForm()
    comment_form = CommentForm()
    notif_count = request.user.notifications.filter(is_read=False).count()
    saved_post_ids = request.user.saved_posts.values_list('post_id', flat=True)

    if request.method=='POST': # 2
        if 'post_submit' in request.POST:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid(): #3
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.save()
                return redirect('feed')
            
        elif 'comment_submit' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                Notification.objects.create(
                    to_user = post.author,
                    from_user = request.user, 
                    notification_type = 'comment',
                    post = post,
                    comment = comment
                )
                messages.success(request, "Your comment was added!")
                return redirect('feed')
            

    return render(request, 'network/feed.html', {'posts': posts, 'form': post_form, 'comment_form': comment_form, 'notif_count': notif_count, 'saved_post_ids': saved_post_ids})

    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else: 
        form = UserCreationForm()
    return render(request, 'network/signup.html', {'form': form})

def toggle_like(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        messages.info(request, "You unliked the post.")
    else: 
        post.likes.add(request.user)
        Notification.objects.create(
            to_user=post.author,
            from_user=request.user,
            notification_type='like',
            post=post
        )
        messages.success(request, "You liked the post.")

    return HttpResponseRedirect(reverse('feed'))


@login_required
def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    profile= user_profile.profile
    posts= user_profile.post_set.all().order_by('-created_at')
    is_following = request.user in profile.followers.all()
    saved_count = user_profile.saved_posts.count()

    if request.method == 'POST':
        if is_following:
            profile.followers.remove(request.user)
        else: 
            profile.followers.add(request.user)
        return redirect('profile', username=username)
    return render(request, 'network/profile.html', {
        'profile_user': user_profile,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
        'saved_count': saved_count,
    })

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'network/edit_profile.html', {'form': form})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect('feed')
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'network/edit_comment.html', {'form': form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden("You cannot delete this comment.")
    if request.method == 'POST':
        Notification.objects.filter(comment=comment).delete()
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect('feed')
    return render(request)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to deleter this post.")
    if request.method == 'POST':
        Notification.objects.filter(post=post).delete()
        post.delete()
        return redirect('feed')
    return render(request, 'network/confirm_delete.html', {'post': post})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user!= post.author:
        return redirect('feed')
    if request.method =='POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form=PostForm(instance=post)
        return render(request, 'network/edit_post.html', {'form': form, 'post': post})

def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = get_object_or_404(Profile, user=target_user)
    current_profile = request.user.profile
    if request.user in target_profile.followers.all():
        target_profile.followers.remove(request.user)
    else:
        target_profile.followers.add(request.user)
        Notification.objects.create(
            to_user = target_user,
            from_user = request.user,
            notification_type = 'follow'
        )
        messages.success(request, f"You followed {target_user.username}.")
    return redirect('profile', username=username)

@login_required
def inbox(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'messages/inbox.html', {'users': users})
@login_required
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        recipient__in=[request.user, other_user]
    ).order_by('timestamp')

    Message.objects.filter(sender=other_user, recipient=request.user, is_read=False).update(is_read=True)
    return render(request, 'messages/chat.html', {
        'other_user': other_user,
        'messages': messages
    })

@login_required
def send_message(request, username):
    if request.method== 'POST':
        recipient = get_object_or_404(User, username=username)
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content or image:
            Message.objects.create(sender=request.user, recipient=recipient, content=content, image=image)
            Notification.objects.create(
                to_user = recipient,
                from_user = request.user,
                notification_type = 'message'
            )
            messages.success(request, f"Message sent to {recipient.username}!")
    return redirect('chat', username=username)

@login_required 
def notifications_view(request):
    notifs = request.user.notifications.all().order_by('-timestamp')
    notifs.update(is_read=True)
    return render(request, 'network/notifications.html', {'notifications': notifs})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    comment_form = CommentForm()

    return render(request, 'network/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def toggle_save(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    saved_post, created = SavedPost.objects.get_or_create(user=request.user, post=post)
    if not created:
        saved_post.delete()
        messages.success(request, "Post removed from saved.")
    else:
        messages.success(request, "Post saved!")
    return redirect('feed')

@login_required
def saved_posts_view(request, username):
    user = get_object_or_404(User, username=username)
    saved_post_ids = user.saved_posts.values_list('post_id', flat=True)
    posts = Post.objects.filter(id__in=saved_post_ids).order_by('-created_at')
    return render(request, 'network/saved_posts.html', {'saved_user': user, 'posts': posts})


