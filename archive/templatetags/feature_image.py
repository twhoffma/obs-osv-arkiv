from django.template import Library

import archive.models

register = Library()

@register.inclusion_tag('archive/feature_image.html')
def feature_image(item, node):
    if item == '':
        filename = None
        mime_type = None
    else:
        if item.itemmedia_set.all().count() > 0:
            itemmedia = item.itemmedia_set.all().order_by('order')[0]
            media = itemmedia.media
            file = media.filename
            filename = media.filename.name
        else:
            filename = None
            file = None
            media = None
    return {
        'filename': filename,
        'file': file,
        'item': item,
        'node': node,
        'num_macro': item.itemmedia_set.filter(media__macro_zoom=True).count(),
        'num_movies': item.itemmedia_set.filter(media__media_type=archive.models.Media.MEDIA_TYPE_MOVIE).count(),
        'icon_color': media.icon_color_name() if media else None,
        'm': media
    }
