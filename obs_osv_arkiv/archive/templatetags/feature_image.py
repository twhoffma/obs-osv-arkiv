from django.template import Library
import pdb

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
	return({'filename': filename, 'file': file, 'item': item, 'node': node})
