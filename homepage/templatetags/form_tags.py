from django import template

register = template.Library()

@register.filter(name='add_attrs')
def add_attrs(field, attrs_string):
    # Parses the attribute string "key:value,key2:value2" into a dictionary
    try:
        attrs = dict(pair.split(':', 1) for pair in attrs_string.split(','))
    except ValueError:
        # Handle cases where parsing might fail, though basic validation is expected in usage
        attrs = {}
    return field.as_widget(attrs=attrs) 