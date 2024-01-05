from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment


user1 = User.objects.create_user('user1')
user2 = User.objects.create_user('user2')


author1 = Author.objects.create(user=user1, rating=0)
author2 = Author.objects.create(user=user2, rating=0)


category1 = Category.objects.create(name='Спорт')
category2 = Category.objects.create(name='Политика')
category3 = Category.objects.create(name='Образование')
category4 = Category.objects.create(name='Технологии')


post1 = Post.objects.create(author=author1, post_type='article', title='Статья 1', content='Содержание статьи 1', rating=0)
post2 = Post.objects.create(author=author2, post_type='article', title='Статья 2', content='Содержание статьи 2', rating=0)
post3 = Post.objects.create(author=author1, post_type='news', title='Новость 1', content='Содержание новости 1', rating=0)


post1.categories.add(category1, category2)
post2.categories.add(category3, category4)
post3.categories.add(category1, category3)


comment1 = Comment.objects.create(post=post1, user=user1, text='Комментарий 1', rating=0)
comment2 = Comment.objects.create(post=post2, user=user2, text='Комментарий 2', rating=0)
comment3 = Comment.objects.create(post=post3, user=user1, text='Комментарий 3', rating=0)
comment4 = Comment.objects.create(post=post1, user=user2, text='Комментарий 4', rating=0)


post1.like()
post2.dislike()
comment1.like()
comment3.dislike()


author1.update_rating()
author2.update_rating()


best_user = Author.objects.all().order_by('-rating').first()
print(f"Лучший пользователь: {best_user.user.username}, Рейтинг: {best_user.rating}")


best_post = Post.objects.filter(post_type='article').order_by('-rating').first()
print(f"Лучшая статья: {best_post.created_at}, Автор: {best_post.author.user.username}, Рейтинг: {best_post.rating}, Заголовок: {best_post.title}, Превью: {best_post.preview()}")


comments_to_best_post = Comment.objects.filter(post=best_post)
for comment in comments_to_best_post:
    print(f"Дата: {comment.created_at}, Пользователь: {comment.user.username}, Рейтинг: {comment.rating}, Текст: {comment.text}")