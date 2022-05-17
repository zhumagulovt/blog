from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(
        verbose_name='Фото профиля', upload_to='photos/profile/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class UserFollowing(models.Model):

    user_id = models.ForeignKey(User, related_name='following', blank=True, null=True, on_delete=models.CASCADE)

    following_user_id = models.ForeignKey(User, related_name='followers', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user_id', 'following_user_id'] 