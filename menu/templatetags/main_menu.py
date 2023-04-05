from django import template

from menu.models import Menu, SuperMenu

register = template.Library()


@register.inclusion_tag('menu/menu.html')
def draw_menu(name):
    super_parent = SuperMenu.objects.get(name=name)
    return {'parent': super_parent}


@register.simple_tag
def draw(name):
    super_parent = SuperMenu.objects.get(name=name)
    menu_list = Menu.objects.all().filter(super_parent=super_parent)

    def tree(objects):
        nesting = min([obj.level for obj in objects])
        layer = [obj for obj in objects if obj.level == nesting]
        _tree = []

        for obj in layer:
            child = get_child(menu_list, obj)
            obj.child = tree(child) if child else []
            _tree.append(obj)

        return _tree

    return tree(menu_list) if menu_list else []


def get_child(list, obj):
    child_list = []
    for i in list:
        if i.parent_id == obj.id:
            child_list.append(i)
        else:
            pass
    return child_list
