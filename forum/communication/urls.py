from django.urls import path

from communication.views import (add_topic, change_topic, delete_topic,
                                 detail_topic, main_forum, profile_topic,
                                 rubric_detail)

urlpatterns = [
    path('rubric/<int:pk>', rubric_detail, name='rubric_detail'),
    path('topic/<int:pk>/', profile_topic, name='profile_topic'),
    path('create_topic', add_topic, name='create_topic'),
    path('change_topic<int:pk>', change_topic, name='change_topic'),
    path('delete_topic<int:pk>', delete_topic, name='delete_topic'),
    path('<int:pk>/', detail_topic, name='detail_topic'),
    path('', main_forum, name='forum_main'),
]
