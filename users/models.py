from django.contrib.auth.models import AbstractUser
from django.db import models


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
    image = models.ImageField(upload_to='users/')
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        error_messages={
            'unique': 'A user with that username already exists.',
        },
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email
