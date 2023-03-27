from django import template

register = template.Library()

@register.simple_tag
def calculate_total_sum(orders):
    total_sum = sum(order.total_cost for order in orders)
    return total_sum
