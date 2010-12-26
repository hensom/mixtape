from django.conf.urls.defaults import *
from mixtape.ui.mixtape_main   import views

urlpatterns = patterns('',
  url(r'^$',                                  views.root,    name = 'root'),
  url(r'^source/(?P<source_id>\w+)/preview$', views.preview, name = 'preview'),
  url(r'^source/(?P<source_id>\w+)/new$',     views.new,     name = 'new'),
  url(r'^playlist/(?P<playlist_id>[^\/]+)/$', views.playlist_view,      name = 'playlist-view'),
  url(r'^playlist/(?P<playlist_id>[^\/]+)/format/(?P<format>[^\/]+)/$', views.playlist_serialize,    name = 'playlist-serialize'),
)