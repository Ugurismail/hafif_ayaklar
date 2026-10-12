import bleach
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe


register = template.Library()


def _message_link_attributes(attrs, new=False):
    href = attrs.get((None, 'href'), '')
    if href.startswith(('http://', 'https://')):
        attrs[(None, 'target')] = '_blank'
        attrs[(None, 'rel')] = 'nofollow noopener noreferrer'
    return attrs


@register.filter
def message_links(value):
    # Messages are plain text, even when a caller passes a SafeString.
    return mark_safe(bleach.linkify(
        escape(str(value)),
        callbacks=[_message_link_attributes],
        parse_email=True,
    ))
