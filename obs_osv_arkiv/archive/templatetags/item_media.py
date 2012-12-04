from django.template import Library
import pdb

register = Library()

@register.inclusion_tag('archive/item_media.html')
def item_media(item):
	media = []
	if item:
			itemmedia = item.itemmedia_set.all().order_by('order')
			media = [m.media for m in itemmedia]
	return({'media': media})
