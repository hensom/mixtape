import urllib2

from datetime                     import datetime
from django.core.urlresolvers     import reverse
from django.http                  import HttpResponseRedirect, HttpResponse
from django.shortcuts             import render_to_response
from mongoengine.django.shortcuts import get_document_or_404
from mixtape                      import sources, serializers
from mixtape.models               import Playlist

def root(request):
  sources_info = [ ]
  
  for source in sources.sources():
    sources_info.append({
      'source': source,
      'form':   source.configuration_form()
    })
    
  sources_info.sort(lambda s: s['source'].name())
  
  playlists = []
  
  for playlist in Playlist.objects.all():
    source = sources.source_with_id(playlist.source_id)

    playlists.append({
      'playlist':      playlist,
      'source':        source,
      'configuration': source.configuration_preview_html(playlist.configuration)
    })

  context = {
    'sources':   sources_info,
    'playlists': playlists
  }
  
  return render_to_response('mixtape_main/root.html', context)
  
def preview(request, source_id):
  source   = sources.source_with_id(source_id)
  
  form     = source.configuration_form(data = request.REQUEST)
  previews = []
  
  if form.is_valid():
    conf     = form.configuration()
    previews = [source.preview_html(t) for t in source.tracks(conf, number = 10)]
    
  context = {
    'source':   source,
    'form':     form,
    'previews': previews
  }
  
  return render_to_response('mixtape_main/preview.html', context)
  
def new(request, source_id):
  source = sources.source_with_id(source_id)
  
  form   = source.configuration_form(data = request.POST)

  if form.is_valid():    
    playlist = Playlist(source_id = source_id, configuration = form.configuration())
    
    playlist.save()
    
    return HttpResponseRedirect(reverse('playlist-view', kwargs = {'playlist_id': str(playlist.pk)}))
  else:
    return preview(request, source_id)
    
def playlist_view(request, playlist_id):
  playlist        = get_document_or_404(Playlist, id = playlist_id)
  source          = sources.source_with_id(playlist.source_id)
  all_serializers = serializers.serializers()

  all_serializers.sort(key = lambda s: s.name())
  
  context = {
    'playlist':      playlist,
    'configuration': source.configuration_preview_html(playlist.configuration),
    'source':        source,
    'serializers':   all_serializers
  }
  
  return render_to_response('mixtape_main/playlist_view.html', context)

def playlist_serialize(request, playlist_id, format):
  playlist   = get_document_or_404(Playlist, id = playlist_id)
  serializer = serializers.serializer_with_id(format)(playlist.tracks)
  
  return HttpResponse(serializer, mimetype = serializer.mimetype())