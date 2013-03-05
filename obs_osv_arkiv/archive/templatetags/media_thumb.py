from django.template import Library
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer
import os.path

register = Library()

@register.simple_tag
def media_thumb(media, width, height):
    if media.filename and os.path.exists(media.filename.path):
        thumbnailer = get_thumbnailer(media.filename)
        try:
            thumb = thumbnailer.get_thumbnail({'size': (width, height)})
            thumb_url = thumb.url
            return thumb_url
        except:
            pass

    thumb_url = settings.STATIC_URL + 'images/'
    
    if media.media_type == 'Image':
        thumb_url = thumb_url + 'thumb_image.jpg'
    elif media.media_type == 'Movie':
        thumb_url = thumb_url + 'thumb_movie.jpg'
    elif media.media_type == 'Sound':
        thumb_url = thumb_url + 'thumb_audio.jpg'
    elif media.media_type == 'Text':
        thumb_url = thumb_url + 'thumb_text.jpg'
    else:
        thumb_url = thumb_url + 'thumb_misc.jpg'
    return(thumb_url)
