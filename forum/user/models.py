from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from user.utilites import get_timestamp


class User(AbstractUser):
    is_activated = models.BooleanField(default=False, verbose_name='Has been activated?')
    send_messages = models.BooleanField(default=True, verbose_name='Send messages?')
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to=get_timestamp)

    class Meta:
        pass


class Dialog(models.Model):
    members = models.ManyToManyField(User, verbose_name='Members')


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    is_readed = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f'{self.message} | {self.author}'


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification for {self.user.email}'

    def send_verification_email(self):
        link = reverse('email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Account verification for {self.user.username}'
        message = 'To verify your account for {}, follow the link:{}'.format(self.user.email, verification_link)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
