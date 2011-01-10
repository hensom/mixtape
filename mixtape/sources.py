import re
import urllib2
import logging
from datetime       import datetime
from django         import forms
from tempfile       import SpooledTemporaryFile
from mixtape        import models

from hachoir_parser      import guessParser
from hachoir_metadata    import extractMetadata
from hachoir_core.stream import InputIOStream

TEXT_LINK = re.compile('(?P<url>http[s]?:\/\/[^\s]+)', re.I)

PLAYLIST_SOURCES = { }

LOG = logging.getLogger(__name__)

def register_source(source_class):
  if source_class.id() in PLAYLIST_SOURCES:
    raise Exception("%s has already been registered as a playlist source" % source_class.id())
  else:
    PLAYLIST_SOURCES[source_class.id()] = source_class
    
def sources():
  return PLAYLIST_SOURCES.values()
  
def source_with_id(source_id):
  return PLAYLIST_SOURCES[source_id]

class Track(object):
  def __init__(self, reference_key = None, urls = None, object = None):
    self.reference_key = reference_key
    self.object        = object
    self.urls          = urls or []
    
  @classmethod
  def urls_from_text(cls, text):
    urls = []
    for match in TEXT_LINK.finditer(text):
      urls.append(match.group('url'))
    return urls
    
class PlaylistConfigurationForm(forms.Form):
  def configuration(self):
    raise NotImplementedError()

class PlaylistSource(object):
  @classmethod
  def id(self):
    raise NotImplementedError()

  @classmethod
  def name(self):
    raise NotImplementedError()

  @classmethod
  def configuration_form(self, configuration = None, **form_args):
    raise NotImplementedError()

  @classmethod
  def tracks(self, configuration, num = 10):
    raise NotImplementedError()

  @classmethod
  def track_preview_html(self, track):
    raise NotImplementedError()

  @classmethod
  def configuration_preview_html(self, configuration):
    raise NotImplementedError()
    
class PlaylistSync(object):    
  def sync(self, playlist):
    source      = source_with_id(playlist.source_id)
    prev_tracks = dict((t.reference_key, t) for t in playlist.tracks)
    track_list  = []

    for track in source.tracks(playlist.configuration):
      new_track = prev_tracks.get(track.reference_key)
      
      if not new_track:
        new_track = self.get_track(track)

      if new_track:
        track_list.append(new_track)

    playlist.tracks = track_list
    playlist.last_sync_date = datetime.now()
    playlist.save()
        
  def download_url(self, url):
    f   = urllib2.urlopen(url)
    tmp = SpooledTemporaryFile()
    tmp.writelines(f)
    return tmp
    
  def get_track(self, track):
    for url in track.urls:
      f, parser = None, None

      try:
        f      = self.download_url(url)
        parser = guessParser(InputIOStream(f))
      except Exception, e:
        LOG.exception('Unable to handle url: %s' % url)
        continue

      if parser:
        metadata  = extractMetadata(parser)
        new_track = models.Track(reference_key = track.reference_key, url = url)
        new_track.title    = metadata.get('title')
        new_track.artist   = metadata.get('author')
        new_track.duration = 24 * 60 * 60 * metadata.get('duration').days + metadata.get('duration').seconds
        return new_track

    return None
