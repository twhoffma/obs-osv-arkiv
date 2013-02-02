from django.template import Library
import os.path
import pdb

register = Library()

@register.inclusion_tag('archive/media_details.html')
def media_details(media):
	if media == '' or not os.path.exists(media.filename.path):
		filename = ''
		mime_type = ''
		file = ''
		msg = 'Warning: Attached file not found'
	else:
		file = media.filename
		filename = media.filename.name
		mime_type = media.media_type
		msg = ''
	return({'filename': filename, 'mime': mime_type, 'file': file, 'm': media, 'msg': msg})
