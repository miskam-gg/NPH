from django.shortcuts import render, get_object_or_404
from .models import Post

def news_list(request):
    news_list = Post.objects.filter(post_type='news').order_by('-created_at')
    context = {'news_list': news_list}
    return render(request, 'news/news_list.html', context)

def news_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'news/news_detail.html', context)
