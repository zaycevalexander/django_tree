from django.db import models

from user.models import User


class Rubric(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f'{self.name}'


class Topic(models.Model):
    title = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    context = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET('User delete'))
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}  | {self.rubric}'


class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.CharField(max_length=64)
    content = models.TextField()
    is_active = models.BooleanField(default=True, db_index=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_date']
