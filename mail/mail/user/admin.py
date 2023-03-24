from django.contrib import admin

from user.models import Email_to_sending, File, User

admin.site.register(User)
admin.site.register(Email_to_sending)
admin.site.register(File)
