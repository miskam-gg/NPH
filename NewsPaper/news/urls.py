from django.urls import path
from .views import news_list, news_detail, news_search, PostCreateView, PostUpdateView, PostDeleteView

app_name = 'news'

urlpatterns = [
    path('news/', news_list, name='news_list'),
    path('news/<int:post_id>/', news_detail, name='news_detail'),
    path('news/search/', news_search, name='news_search'),
]
