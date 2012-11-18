from django.template import Library

register = Library()

@register.inclusion_tags('media_details.html')
def media_details(media):
	details = []
	details['filename'] = media.filename.filename
	details['mime-type'] = media.media_type
	return({'details': details})
