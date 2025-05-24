from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from posts.models import Post

def is_admin(user):
    return user.is_authenticated and user.is_admin

@user_passes_test(is_admin)
def approve_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.approved = True
    post.save()
    return redirect('unapproved-posts')

def main(request):
    user = request.user
    posts = Post.objects.filter(approved=True).order_by('-created_at')
    return render(request, "home.html", {
        "user":user,
        "posts":posts
    })

def posts_unapproved(request):
    user = request.user
    if user.is_authenticated and user.is_admin:
        posts = Post.objects.filter(approved=False).order_by('-created_at')
        return render(request, "posts/approve.html", {
            "user": user,
            "posts":posts
        })