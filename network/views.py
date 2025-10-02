from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse

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
# Create your views here.

