from captcha.fields import CaptchaField
from django import forms

from communication.models import Comment, Topic


class UserCommentField(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['is_active']
        widgets = {'topic': forms.HiddenInput}


class GuestCommentField(forms.ModelForm):
    captcha = CaptchaField(label='Enter text from image', error_messages={'invalid': 'Wrong text'})

    class Meta:
        model = Comment
        exclude = ['is_active']
        widgets = {'topic': forms.HiddenInput}


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ['created_date']
        widgets = {'author': forms.HiddenInput}
