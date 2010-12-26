from django.conf.urls.defaults import *

from django.conf import settings

urlpatterns = patterns('',
  url(r'^', include('mixtape.ui.mixtape_main.urls')),
)

if settings.DEBUG:
  urlpatterns += patterns('',
    url(r'^static/(?:[^\/]+)/(?P<path>.*)$',   'django.views.static.serve', {'document_root': settings.STATIC_BASE_DIR})
  )