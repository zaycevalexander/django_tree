from django.urls import path

from user.views import (UserlogoutView, UserRegisterDoneView,
                        UserRegistrationView, profile, upload_file)

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('registration/successful', UserRegisterDoneView.as_view(), name='register_done'),
    path('logout/', UserlogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', profile, name='profile'),
    path('profile/upload_file/', upload_file, name='upload_file'),
]
