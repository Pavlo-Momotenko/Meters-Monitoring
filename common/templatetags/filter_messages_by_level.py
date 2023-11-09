from django import template

register = template.Library()


@register.filter
def filter_messages_by_level(messages, level):
    return [message for message in messages if message.level == level]
