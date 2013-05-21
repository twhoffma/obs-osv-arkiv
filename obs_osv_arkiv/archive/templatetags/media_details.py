from django import template
import os.path

register = template.Library()

@register.inclusion_tag('archive/media_details.html')
def media_details(media):
    try:
        if not os.path.exists(media.filename.path):
            raise Exception('File is gone!')
        file = media.filename
        filename = media.filename.name
        mime_type = media.media_type
        msg = ''
    except Exception, e:
        filename = ''
        mime_type = ''
        file = ''
        msg = 'Warning: Attached file not found (' + e.message + ')'
    return({'filename': filename, 'mime': mime_type, 'file': file, 'm': media, 'msg': msg})
