from django.views.generic import TemplateView


class MenuMain(TemplateView):
    template_name = 'menu/base.html'
