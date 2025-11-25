from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='url_to_font_name')
def url_to_font_name(value):
    """Convert Google Fonts URL format (EB+Garamond) to CSS format (EB Garamond)"""
    if value:
        return value.replace('+', ' ')
    return value

@register.filter(name='is_system_font')
def is_system_font(value):
    """Check if font is a system font (doesn't need Google Fonts)"""
    system_fonts = [
        'Georgia',
        'Times+New+Roman',
        'Book+Antiqua',
        'Courier+New',
        'Comic+Sans+MS',
        'Arial',
        'Verdana',
        'Helvetica'
    ]
    return value in system_fonts

