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
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('follow/<str:username>/', views.follow_toggle, name='follow_toggle'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)