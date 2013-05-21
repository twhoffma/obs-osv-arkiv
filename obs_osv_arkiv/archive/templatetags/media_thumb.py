from django.template import Library
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer
import os.path

register = Library()

@register.simple_tag
def media_thumb(media, width, height):
    return media.thumbnail(width, height)
