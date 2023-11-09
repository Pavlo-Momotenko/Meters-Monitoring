from django import template

register = template.Library()


@register.filter
def total_sum(data, column_name):
    return sum([value[column_name] for value in data])
