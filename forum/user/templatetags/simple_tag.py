from django import template

register = template.Library()


@register.simple_tag()
def get_companion(user, dialog):
    for u in dialog.members.all():
        if u != user:
            return u
    return None
