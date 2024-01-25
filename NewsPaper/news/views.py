from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView,CreateView
from django.urls import reverse_lazy
from .models import Profile,Post
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profile/edit_profile.html'

    fields = ['field1', 'field2']

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('profile_detail')

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

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile_detail.html'


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile_detail')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def become_author(request):
    if request.method == 'POST':
        author_group = Group.objects.get(name='authors')
        request.user.groups.add(author_group)
        return redirect('success_page')
    return render(request, 'become_author.html')

class CreatePostView(PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'create_post.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class EditPostView(PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'edit_post.html'
    permission_required = 'news.change_post'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)