import logging
import os
from fcntl                       import flock, LOCK_EX, LOCK_UN, LOCK_NB
from datetime                    import datetime, timedelta
from django.conf                 import settings
from django.core.management.base import BaseCommand
from mixtape.sources             import PlaylistSync
from mixtape.models              import Playlist

LOG = logging.getLogger(__name__)

class Command(BaseCommand):
  def handle(self, *args, **options):  
    lockfile = os.path.join(settings.LOCK_DIR, 'sync-playlists.lock')

    lock = open(lockfile, 'w+')

    try:
      flock(lock, LOCK_EX | LOCK_NB)
    except IOError:
      return

    resync_time = datetime.now() - timedelta(hours = 1)
    manager = PlaylistSync()

    for playlist in Playlist.objects.all():
      if True or playlist.last_sync_date is None or playlist.last_sync_date < resync_time:
        try:
          manager.sync(playlist)
        except:
          LOG.exception('Unable to sync playlist: %s' % playlist.id)
            
    flock(lock, LOCK_UN)
    lock.close()
