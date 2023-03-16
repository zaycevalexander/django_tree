# Generated by Django 3.2.13 on 2023-02-21 09:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=models.SET('User deleted'), to=settings.AUTH_USER_MODEL),
        ),
    ]
