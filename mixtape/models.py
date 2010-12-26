import                           logging
from datetime             import datetime, timedelta
from mongoengine          import Document, EmbeddedDocument
from mongoengine          import IntField, FloatField, DateTimeField, ListField
from mongoengine          import DictField, BooleanField, URLField
from mongoengine          import EmbeddedDocumentField, ObjectIdField, StringField
from mongoengine.base     import ValidationError

logger = logging.getLogger(__name__)

class Track(EmbeddedDocument):
  artist        = StringField()
  title         = StringField(required = True)
  duration      = IntField(required = True)
  url           = StringField(required = True)
  reference_key = StringField(required = True)
  
  def display_title(self):
    if self.artist:
      return '%s - %s' % (self.artist, self.title)
    else:
      return self.title
  
class PlaylistConfiguration(EmbeddedDocument):
  pass

class Playlist(Document):
  source_id      = StringField(required = True)
  configuration  = EmbeddedDocumentField(PlaylistConfiguration)
  tracks         = ListField(EmbeddedDocumentField(Track), default = lambda: [])
  creation_date  = DateTimeField(required = True, default = lambda: datetime.now())
  last_sync_date = DateTimeField()