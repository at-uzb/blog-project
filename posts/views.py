from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, F, IntegerField, ExpressionWrapper
from .models import Post, Like
from .forms import PostForm, CommentForm
from django.utils import timezone
from datetime import timedelta
import random
from django.contrib.auth.decorators import login_required

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    session_key = f"viewed_post_{pk}"
    if not request.session.get(session_key, False):
        post.view_count = F('view_count') + 1
        post.save(update_fields=['view_count'])
        request.session[session_key] = True
        post.refresh_from_db() 

    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('posts:post-detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('posts:post-detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/post.html', {'form': form})


def filtered_posts(request):
    user = request.user
    filter_by = request.GET.get('filter', 'latest')

    posts = Post.objects.filter(approved=True)

    if filter_by == 'most_viewed':
        posts = posts.order_by('-view_count')
    # elif filter_by == 'weekly':
    #     last_week = timezone.now() - timedelta(days=7)
    #     posts = posts.filter(created_at__gte=last_week).order_by('-created_at')
    # elif filter_by == 'monthly':
    #     last_month = timezone.now() - timedelta(days=30)
    #     posts = posts.filter(created_at__gte=last_month).order_by('-created_at')

    elif filter_by == 'weekly':
        last_week = timezone.now() - timedelta(days=7)
        posts = posts.filter(created_at__gte=last_week).annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
            score=ExpressionWrapper(
                F('likes_count') + F('comments_count') + F('view_count'),
                output_field=IntegerField()
            )
        ).order_by('-score', '-created_at')

    elif filter_by == 'monthly':
        last_month = timezone.now() - timedelta(days=30)
        posts = posts.filter(created_at__gte=last_month).annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
            score=ExpressionWrapper(
                F('likes_count') + F('comments_count') + F('view_count'),
                output_field=IntegerField()
            )
        ).order_by('-score', '-created_at')
    elif filter_by == 'most_recommended':
            posts = list(posts) 
            random.shuffle(posts)                      
            posts = posts[:10]  
    else:
        posts = posts.order_by('-created_at')

    return render(request, 'home.html', {
        'posts': posts,
        "user":user
        })

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(post=post, author=request.user)

    if not created:
        like.delete()

    return redirect(request.META.get('HTTP_REFERER', 'posts:post-list'))