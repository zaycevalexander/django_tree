from django import forms
from django.contrib.auth.forms import UserCreationForm

from user.models import Email_to_sending, File, User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ['created_date']
        widgets = {'user': forms.HiddenInput}


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email_to_sending
        fields = ('subject', 'message', 'name_author', 'author')
        widgets = {'author': forms.HiddenInput}
