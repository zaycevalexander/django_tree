from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=32, verbose_name='Phone number')


class File(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='%Y/%m/%d/', null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}'


class Email_to_sending(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=256)
    message = models.TextField()
    name_author = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.author} | {self.subject}'

    class Meta:
        verbose_name = 'Email to sending'
