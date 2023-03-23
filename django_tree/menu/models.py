from django.db import models
from django.conf import settings


class SuperMenu(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Super menu'
        verbose_name_plural = 'Super menu'

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='menu_item')
    slug = models.SlugField(max_length=128)
    level = models.IntegerField(default=1)
    super_parent = models.ForeignKey(SuperMenu, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'menu'
        verbose_name_plural = 'menu'
        ordering = ['level']

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = get_menu_item_id(self)
        self.url = set_url(self)


def get_menu_item_id(self) -> int:
    if not self.parent:
        return 1
    else:
        return self.parent.level + 1


def set_url(self):
    if settings.ALLOWED_HOSTS and not self.parent:
        return f'http://{settings.ALLOWED_HOSTS[0]}/{self.slug}'
    else:
        return f'{self.parent.url}/{self.slug}'
