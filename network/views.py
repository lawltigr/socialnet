from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import EditProfileForm
from django.contrib.auth.models import User

@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    post_form = PostForm()
    comment_form = CommentForm()

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
                return redirect('feed')
            

    return render(request, 'network/feed.html', {'posts': posts, 'form': post_form, 'comment_form': comment_form})
    
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
    else: 
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('feed'))


@login_required
def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    profile= user_profile.profile
    posts= user_profile.post_set.all().order_by('-created_at')
    is_following = request.user in profile.followers.all()

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
