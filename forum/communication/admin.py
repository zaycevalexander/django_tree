from django.contrib import admin

from communication.models import Comment, Rubric, Topic

admin.site.register(Rubric)
admin.site.register(Topic)
admin.site.register(Comment)
