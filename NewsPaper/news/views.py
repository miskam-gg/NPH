from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post
from .filters import PostFilter

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news:news_list')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news:news_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('news:news_list')

def news_list(request):
    news_list = Post.objects.filter(post_type='news').order_by('-created_at')
    paginator = Paginator(news_list, 10)

    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    context = {'news': news}
    return render(request, 'news/news_list.html', context)

def news_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'news/news_detail.html', context)

def news_search(request):
    filter = PostFilter(request.GET, queryset=Post.objects.all())
    context = {'filter': filter}
    return render(request, 'news/news_search.html', context)