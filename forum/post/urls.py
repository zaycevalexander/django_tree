from django.urls import path

from post.views import detail

urlpatterns = [
    path('<int:pk>', detail, name='detail'),
]
