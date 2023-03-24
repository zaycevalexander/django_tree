from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.views.generic.edit import DeleteView, UpdateView
from twilio.rest import Client

from user.forms import ChangeUserForm, MessageForm, UserRegistrationForm
from user.models import Dialog, EmailVerification, User


class RegisterUserView(CreateView):
    model = User
    template_name = 'user/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register_done')


class EmailVerificationView(TemplateView):
    template_name = 'user/verified_email.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_activated = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('forum_main'))


class RegisterDoneView(TemplateView):
    template_name = 'user/register_done.html'


class LoginUserView(LoginView):
    template_name = 'user/login.html'


class LogoutUserView(LoginRequiredMixin, LogoutView):
    template_name = 'user/logout.html'


class ChangeUserFormInfo(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user/change_user_info.html'
    form_class = ChangeUserForm
    success_url = reverse_lazy('forum_main')
    success_message = 'Data changed successfully'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


@login_required
def profile(request, pk):
    user = User.objects.get(pk=pk)
    context = {
        'user': user
    }
    return render(request, 'user/profile.html', context)


class PasswordUserChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'user/change_password.html'
    success_message = 'Change password'
    success_url = reverse_lazy('user_profile')


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'user/delete_user.html'
    success_url = reverse_lazy('forum_main')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User deleted')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class DialogsView(View):
    def get(self, request):
        dialog = Dialog.objects.filter(members__in=[request.user.id])
        context = {
            'dialog': dialog,
            'user_profile': request.user
        }
        return render(request, 'user/dialogs.html', context)


class MessagesView(View):
    def get(self, request, dialog_id):
        try:
            dialog = Dialog.objects.get(id=dialog_id)
            if request.user in dialog.members.all():
                dialog.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                dialog = None
        except Dialog.DoesNotExist:
            dialog = None
        context = {
            'user_profile': request.user,
            'dialog': dialog,
            'form': MessageForm()
        }
        return render(request, 'user/messages.html', context)

    def post(self, request, dialog_id):
        recipient_pk = 0
        form = MessageForm(data=request.POST)
        recipient = Dialog.objects.get(id=dialog_id).members.all().exclude(id=request.user.pk)
        for a in recipient:
            recipient_pk = a.id
        user = User.objects.get(id=recipient_pk)
        if form.is_valid() and user.send_messages:
            message = form.save(commit=False)
            message.dialog_id = dialog_id
            message.author = request.user
            message.save()
            if user.phone_number:
                send_message_sms(user.phone_number, f'You received a message from {request.user}')
            return redirect(reverse('messages', kwargs={'dialog_id': dialog_id}))
        else:
            return HttpResponse(f'{user.username} does not receive messages')


class CreateDialogView(View):
    def get(self, request, user_id):
        dialog = Dialog.objects.filter(members__in=[request.user.id, user_id]).annotate(c=Count('members')).filter(c=2)
        if dialog.count() == 0:
            dialog = Dialog.objects.create()
            dialog.members.add(request.user)
            dialog.members.add(user_id)
        else:
            dialog = dialog.first()
        return redirect(reverse('messages', kwargs={'dialog_id': dialog.id}))


def send_message_sms(destination: str, message: str):
    account_sid = 'AC67d9e784dc6a6df3ecafd3e075b0281b'
    auth_token = '1609cae84e7164a5bad30dec9b524a73'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_='+12765971876',
        to=destination
    )
    print(message.sid)
