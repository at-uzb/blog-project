from django.urls import path
from .views import post_create, post_detail, like_post

urlpatterns = [
    path("create/", post_create, name="post-create"),
    path("<int:pk>/", post_detail, name="post-detail"),
    path('like/<int:post_id>/', like_post, name='like-post'),
]