# Generated by Django 2.2.16 on 2021-10-15 11:04

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20211014_1524'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('locations', django.db.models.manager.Manager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='latitude',
            field=models.FloatField(default=56.012269),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='longitude',
            field=models.FloatField(default=92.861473),
            preserve_default=False,
        ),
    ]