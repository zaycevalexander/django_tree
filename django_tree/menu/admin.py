from django.contrib import admin
from menu.models import Menu, SuperMenu

admin.site.register(SuperMenu)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    readonly_fields = ['level']
