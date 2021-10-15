from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.expressions import RawSQL


class LocationManager(models.Manager):
    def nearby(self, latitude, longitude, proximity):
        gcd = """
              6371 * acos(
               cos(radians(%s)) * cos(radians(latitude))
               * cos(radians(longitude) - radians(%s)) +
               sin(radians(%s)) * sin(radians(latitude))
              )
              """
        return self.get_queryset() \
            .exclude(latitude=None) \
            .exclude(longitude=None) \
            .annotate(distance=RawSQL(gcd, (latitude,
                                            longitude,
                                            latitude))) \
            .filter(distance__lt=proximity) \
            .order_by('distance')


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
        blank=True,
    )
    locations = LocationManager()
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email


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
