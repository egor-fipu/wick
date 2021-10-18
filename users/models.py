from PIL import Image, ImageOps
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
        img = Image.open(self.image.path)
        img = ImageOps.exif_transpose(img)

        fixed_height = 500
        width_size = int(fixed_height * img.width / img.height)
        img = img.resize((width_size, fixed_height), Image.ANTIALIAS)
        width, height = (width_size, fixed_height)

        watermark = Image.open('users/media/watermark.png')
        watermark.thumbnail((150, 100))
        mark_width, mark_height = watermark.size
        paste_mask = watermark.split()[3].point(lambda i: i * 50 / 100)
        x = width - mark_width - 10
        y = height - mark_height - 10
        img.paste(watermark, (x, y), mask=paste_mask)
        img.save(self.image.path)


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
