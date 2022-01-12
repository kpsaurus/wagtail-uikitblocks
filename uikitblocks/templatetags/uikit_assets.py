from django import template

register = template.Library()


@register.inclusion_tag("uikit_js.html")
def uikit_js():
    pass


@register.inclusion_tag("uikit_css.html")
def uikit_css():
    pass
