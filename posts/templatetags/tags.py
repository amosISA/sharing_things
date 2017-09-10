from django import template
import timeago, datetime

register = template.Library()

@register.filter(name="get_time_ago")
def get_time_ago_created_post(value):
    date = datetime.datetime.now()
    time = timeago.format(date, value)
    return time

# So that I can use this filter to add attributes to my elements in templates such as:
# {{ form.email|htmlattributes:"class : something, id: openid_identifier" }}
# So my input email now have a class=something and id=openid_identifier
def htmlattributes(value, arg):
    attrs = value.field.widget.attrs

    data = arg.replace(' ', '')
    kvs = data.split(',')

    for string in kvs:
        kv = string.split(':')
        attrs[kv[0]] = kv[1]

    rendered = str(value)
    return rendered

register.filter('htmlattributes', htmlattributes)