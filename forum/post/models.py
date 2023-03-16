from django.db import models

from user.models import User


class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    author = models.ForeignKey(to=User, on_delete=models.SET('User deleted'))

    def __str__(self):
        return f'{self.title}|{self.created_date}|{self.author}'

    class Meta:
        ordering = ['created_date']
