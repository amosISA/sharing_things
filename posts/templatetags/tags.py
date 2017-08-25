from django import template
import timeago, datetime

register = template.Library()

@register.filter(name="get_time_ago")
def get_time_ago_created_post(value):
    date = datetime.datetime.now()
    time = timeago.format(date, value)
    return time