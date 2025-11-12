from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="posts"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name='post'),
    path('search/', views.search, name='search'),
    path('userposts/', views.UserPostListView.as_view(), name="user_posts"),
    path('usercomments/', views.UserCommentListView.as_view(), name="user_comments"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("posts/new/", views.PostCreateView.as_view(), name="posts_new"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="posts_edit"),
]
