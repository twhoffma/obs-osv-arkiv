from django.forms import MultiValueField, CharField, ChoiceField
from archive.widgets import TopicWidget, LocationWidget, SelectLocationWidget

class TopicField(MultiValueField):
	widget = TopicWidget
	
	def __init__(self, *args, **kwargs):
		fields = (
				CharField(),
				CharField(),
			)
		super(TopicField, self).__init__(fields, *args, **kwargs)
	
	def compress(self, data_list):
		if data_list:
			from archive.models import Topic
			if Topic.objects.filter(topic=data_list[0], subtopic=data_list[1]).count > 0:
				t = Topic.objects.filter(topic=data_list[0], subtopic=data_list[1])[0]
				return(t)
			return None
		return None

#class LocationMultiField(MultiValueField):
#	widget = LocationMultiWidget
#	
#	def __init__(self, *args, *kwargs):
#		fields = (
#				CharField(),
#				CharField(),
#				CharField()
#		)
#		super(LocationMultiField, self).__init__(fields, *args, **kwargs)
#	
#	def compress(self, data_list):
#		pdb.set_trace()
#		if data_list:
#			from archive.models import Location
#			loc = Location.objects.get_or_create(area=data_list[0], room=data_list[1], position_ref=data_list[2])
#			return(loc)
#		return(None)	
				
class LocationField(CharField):
	widget = SelectLocationWidget

	#def __init__(self, *args, **kwargs):
	#	from archive.models import Location
	#			
	#	fields = (
	#			ChoiceField(choices=[(l.area, l.area) for l in Location.objects.all()]),
	#			ChoiceField(choices=[(0, '---')]),
	#			CharField(),
	#		)
	#	super(LocationField, self).__init__(fields, *args, **kwargs)
	
	def compress(self, data_list):
		pdb.set_trace()
		if data_list:
			from archive.models import Location
			if Location.objects.filter(area=data_list[0], room=data_list[1], position_ref=data_list[2]):
				l = Location.objects.get(area=data_list[0], room=data_list[1], position_ref=data_list[2])
				return(l)
			return None
