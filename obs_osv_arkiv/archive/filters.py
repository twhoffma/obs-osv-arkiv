import django_filters
from archive.models import Item

class ItemFilter(django_filters.FilterSet):
	class Meta:
		model = Item
		fields = ['item_number', 'title', 'room']
