from django.contrib import admin

from user.models import EmailVerification, Message, User

admin.site.register(Message)
admin.site.register(User)
admin.site.register(EmailVerification)


class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created_date')
    readonly_fields = ('created_date',)
