from django.template import Library
import pdb

register = Library()

@register.inclusion_tag('archive/media_details.html')
def media_details(media):
	if media == '':
		filename = ''
		mime_type = ''
	else:
		file = media.filename
		filename = media.filename.name
		mime_type = media.media_type	
	return({'filename': filename, 'mime': mime_type, 'file': file, 'm': media})
