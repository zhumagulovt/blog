from statistics import mode
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    content = models.TextField(verbose_name='Контент')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(verbose_name='Фото', upload_to = 'photos/%Y/%m/%d/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('postapp:post-detail', kwargs={'pk': self.pk})


    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']


class Category(models.Model):

    title = models.CharField(max_length=255, verbose_name='Название')

    def get_absolute_url(self):
        return reverse('postapp:category-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['title']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ['-created_at']