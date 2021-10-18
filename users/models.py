from django.contrib.auth.models import AbstractUser
from django.db import models

from .services import watermark_image


class User(AbstractUser):
    FEMALE = 'female'
    MALE = 'male'
    GENDER = [
        (FEMALE, 'женский'),
        (MALE, 'мужской'),
    ]

    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=150)
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.',
        },
    )
    gender = models.CharField(
        'Пол',
        max_length=6,
        choices=GENDER,
    )
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save()
        if not self.image:
            return
        watermark_image(self.image.path)


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Кому нравится'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Кто нравится'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow')
        ]
