SERIALIZERS = { }

def register_serializer(serializer_class):
  if serializer_class.id() in SERIALIZERS:
    raise Exception("%s has already been registered as a serializer" % serializer_class.id())
  else:
    SERIALIZERS[serializer_class.id()] = serializer_class
    
def serializers():
  return SERIALIZERS.values()
  
def serializer_with_id(serializer_id):
  return SERIALIZERS[serializer_id]
  
class Serializer(object):
  def __init__(self, tracks):
    self.tracks = tracks

  @classmethod
  def id(self):
    raise NotImplementedError()

  @classmethod
  def name(self):
    raise NotImplementedError()
    
  @classmethod
  def mimetype(cls):
    raise NotImplementedError()
    
  def __iter_(self):
    raise NotImplementedError()

class M3USerializer(Serializer):
  @classmethod
  def id(cls):
    return 'm3u'
    
  @classmethod
  def name(cls):
    return 'M3U'
    
  @classmethod
  def mimetype(cls):
    return 'audio/x-mpegurl'

  def __iter__(self):
    def serialize():
      yield '#EXTM3U\n'

      for track in self.tracks:
        yield '#EXTINF:%d,%s\n' % (track.duration, track.display_title())
        yield '%s\n' % track.url
      
    return serialize()
    
class PLSSerializer(Serializer):
  @classmethod
  def id(cls):
    return 'pls'
    
  @classmethod
  def name(cls):
    return 'PLS'
    
  @classmethod
  def mimetype(cls):
    return 'audio/x-scpls'

  def __iter__(self):
    def serialize():
      yield '[playlist]\n'
      yield 'NumberOfEntries=%d\n' % len(self.tracks)
      yield 'Version=2\n'
      
      for i, track in enumerate(self.tracks):        
        yield """
File%(num)s=%(url)s
Title%(num)s=%(title)s
Length%(num)s=%(duration)s
        """ % {'num': i + 1, 'url': track.url, 'title': track.display_title(), 'duration': track.duration}
        
    return serialize()
        
register_serializer(M3USerializer)
register_serializer(PLSSerializer)