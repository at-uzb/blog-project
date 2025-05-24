from django.urls import path
from .views import posts_unapproved, approve_post
from posts.views import filtered_posts
urlpatterns = [
    path("", filtered_posts, name="home"),
    path("unapproved-posts/", posts_unapproved, name="unapproved-posts"),
    path("approve/<int:pk>/", approve_post, name="approve-post")
]