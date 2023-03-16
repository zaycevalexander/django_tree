from django.shortcuts import render

from post.models import Post


def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'post/index.html', context)


def detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post
    }
    return render(request, 'post/detail.html', context)
