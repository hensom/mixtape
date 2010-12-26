from django      import template
from django.conf import settings

register = template.Library()

def static_url(base, path, version = None):
  if not version:
    version = settings.RESOURCE_VERSION

  return '%s/%s/%s/%s' % (settings.STATIC_BASE_URL.rstrip('/'), version, base, path)

@register.simple_tag
def css_url(path):
  return static_url('css', path)

@register.simple_tag
def js_url(path):
  return static_url('js', path)