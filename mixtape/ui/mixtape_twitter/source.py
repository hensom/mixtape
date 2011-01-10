from twitter         import Api
from django          import forms
from mongoengine     import StringField
from mixtape.sources import PlaylistSource, PlaylistConfigurationForm, Track
from mixtape.models  import PlaylistConfiguration

class TwitterConfiguration(PlaylistConfiguration):
  query = StringField()

class TwitterConfigurationForm(PlaylistConfigurationForm):
  query = forms.CharField()
  
  def configuration(self):
    return TwitterConfiguration(query = self.cleaned_data['query'])

class TwitterPlaylistSource(PlaylistSource):
  @classmethod
  def id(cls):
    return 'twitter'

  @classmethod
  def name(cls):
    return 'Twitter'

  @classmethod
  def configuration_form(cls, configuration = None, **form_args):
    initial = { }
    if configuration:
      initial['query'] = configuration['query']
      
    form_args = form_args.copy()
    form_args['initial'] = initial
    return TwitterConfigurationForm(**form_args)

  @classmethod
  def preview_html(cls, track):
    return '%s' % track.object.text
    
  @classmethod
  def _track_from_result(cls, result):
    urls = Track.urls_from_text(result.text)
    return Track(reference_key = str(result.id), object = result, urls = urls)

  @classmethod
  def tracks(cls, configuration, number = 10):
    api = Api()
    results = api.GetSearch(configuration.query, per_page = number)
    return [cls._track_from_result(r) for r in results]
    
  @classmethod
  def configuration_preview_html(self, configuration):
    return configuration.query
