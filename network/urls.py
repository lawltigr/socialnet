from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.feed, name='feed'),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
]