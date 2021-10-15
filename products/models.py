from django.db import models


class Category(models.Model):
    title = models.CharField('Название', max_length=200)
    parent_id = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='categories',
        verbose_name='Родительcкая категория'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-id']

    def __str__(self):
        return self.title


class Notebook(models.Model):
    name = models.CharField('Название', max_length=500)
    price = models.FloatField('Цена')
    image = models.SlugField('Ссылка на изображение', max_length=500)
    link = models.SlugField('Ссылка', max_length=500)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='notebooks',
        verbose_name='Категория'
    )
    created = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'
        ordering = ['-created']

    def __str__(self):
        return self.name
