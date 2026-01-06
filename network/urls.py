from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.feed, name='feed'),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('follow/<str:username>/', views.follow_toggle, name='follow_toggle'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('save/<int:post_id>/', views.toggle_save, name='toggle_save'),
    path('saved/', views.saved_posts_view, name='saved_posts'),
    path('saved/<str:username>/', views.saved_posts_view, name='saved_posts'),

    path('messages/', views.inbox, name='inbox'),
    path('messages/<str:username>/', views.chat_view, name='chat'),
    path('messages/<str:username>/send/', views.send_message, name='send_message'),
    path('notifications/', views.notifications_view, name='notifications'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)