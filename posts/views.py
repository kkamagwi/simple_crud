from django.shortcuts import render
from .models import Post
from .forms import PostForm
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect

def index(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})

def posts_detail(request, pk):
    posts_detail = get_object_or_404(Post, pk=pk)
    return render(request, 
                'posts/posts_detail.html', 
                {'posts_detail': posts_detail,})

def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('posts-detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/posts-edit.html', {'form': form})

def post_edit(request, pk):
    posts = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=posts)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('posts-detail', pk=post.pk)
    else:
        form = PostForm(instance=posts)
    return render(request, 'posts/posts_edit.html', {'form': form})

def posts_delete(request, pk):
    try:
        post = Post.objects.get(id=pk)
        post.delete()
        return redirect('posts')
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
