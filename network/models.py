from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    avatar=models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio=models.TextField(blank=True)
    followers=models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return self.user.username
    
    def posts(self):
        return self.user.post_set.all()
    
    
class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    image=models.ImageField(upload_to='posts/', blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f'{self.author.username} - {self.created_at.strftime("%Y-%m-%d %H:%M")}'
    def is_liked_by( self, user):
        return self.likes.filter(id=user.id).exists()
    
class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} on {self.post.id}'
