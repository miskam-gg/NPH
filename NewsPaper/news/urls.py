from django.urls import path
from .views import news_list, news_detail, news_search, PostCreateView, PostUpdateView, PostDeleteView, ProfileDetailView, signup
from django.contrib.auth.views import LoginView
from . import views


app_name = 'news'

urlpatterns = [
    path('news/', news_list, name='news_list'),
    path('news/<int:post_id>/', news_detail, name='news_detail'),
    path('news/search/', news_search, name='news_search'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', signup, name='signup'),
    path('become_author/', views.become_author, name='become_author'),
]
