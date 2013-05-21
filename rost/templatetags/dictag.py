from django import template

register = template.Library()

@register.filter(name='getval')
def getval(dic,key):
    return dic[key]

