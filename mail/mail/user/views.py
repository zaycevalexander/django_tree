from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from user.forms import EmailForm, FileForm, UserRegistrationForm
from user.import_file.excel_reader import ExcelReader
from user.models import Email_to_sending, User


class MainView(TemplateView):
    template_name = 'user/main.html'


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register_done')
    template_name = 'user/registration.html'


class UserRegisterDoneView(TemplateView):
    template_name = 'user/register_done.html'


class UserlogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'user/logout.html'


class UserLoginView(LoginView):
    template_name = 'user/login.html'


@login_required
def profile(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('upload_file')
    else:
        form = EmailForm(initial={'author': request.user.pk})
    context = {
        'user': user,
        'form': form
    }
    return render(request, 'user/profile.html', context)


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            data = request.FILES['file']
            uploading_file = ExcelReader(data)
            base = Email_to_sending.objects.filter(author=request.user.pk).last()
            for email in uploading_file.items:
                send_mail(
                    base.subject,
                    base.message,
                    settings.EMAIL_HOST_USER,
                    [email['email']],
                )
            redirect('main')
    else:
        form = FileForm(initial={'user': request.user.pk})
    return render(request, 'user/upload_file.html', locals())
