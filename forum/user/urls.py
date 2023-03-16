from django.urls import path

from user.views import (ChangeUserFormInfo, CreateDialogView, DeleteUserView,
                        DialogsView, EmailVerificationView, LoginUserView,
                        LogoutUserView, MessagesView, PasswordUserChangeView,
                        RegisterDoneView, RegisterUserView, profile
                        )

urlpatterns = [
    path('registration/', RegisterUserView.as_view(), name='user_registration'),
    path('register_done/', RegisterDoneView.as_view(), name='register_done'),
    path('login/', LoginUserView.as_view(), name='user_login'),
    path('logout/', LogoutUserView.as_view(), name='user_logout'),
    path('delete', DeleteUserView.as_view(), name='user_delete'),
    path('profile/change/password', PasswordUserChangeView.as_view(), name='change_password'),
    path('profile/change/', ChangeUserFormInfo.as_view(), name='user_change_info'),
    path('profile/<int:pk>', profile, name='user_profile'),
    path('dialog/create/<int:user_id>/', CreateDialogView.as_view(), name='dialog_create'),
    path('dialog/<int:dialog_id>/', MessagesView.as_view(), name='messages'),
    path('dialog/', DialogsView.as_view(), name='dialog'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
]
