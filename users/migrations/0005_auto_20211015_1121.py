# Generated by Django 2.2.16 on 2021-10-15 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211015_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
