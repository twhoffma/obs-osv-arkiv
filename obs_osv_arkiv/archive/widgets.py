from django.forms import widgets
from archive.models import Tag

from django.forms.util import flatatt
from django.utils.safestring import mark_safe
import pdb

class TopicWidget(widgets.MultiWidget):
	def __init__(self, attrs=None):
		_widgets = (
			widgets.TextInput(attrs={'class': 'topic'}),
			widgets.TextInput(attrs={'class': 'subtopic'}),
		)
		
		super(TopicWidget, self).__init__(_widgets, attrs)
	
	def decompress(self, value):
		from archive.models import Topic
		if value:
			t = Topic.objects.get(pk=value)
			return([t.topic, t.subtopic])
		return([None, None])

#https://github.com/django/django/blob/master/django/forms/extras/widgets.py
class SelectLocationWidget(widgets.Widget):
	def __init__(self, attrs=None, required=True):
		self.attrs = attrs or {}
		self.required = required
	
	def render(self, name, value, attrs=None):
		#pdb.set_trace()
		from archive.models import Location
		output= []
		
		choices_area = [(l.area, l.area) for l in Location.objects.all()]
		
		if value:
			loc = Location.objects.get(pk=value)
			selected_area = loc.area
			selected_room = loc.room
			selected_pos = loc.position_ref
			
			choices_room = [(l.room, l.room) for l in Location.objects.filter(area=selected_area)]
			pos = loc.position_ref
		else:
			selected_area = choices_area[0][0]
			selected_room = ''
			selected_pos = ''			

		choices_room = [(l.room, l.room) for l in Location.objects.filter(area=selected_area)]
		if selected_room == '':
			selected_room = choices_room[0][0]
		
		s = widgets.Select(choices=choices_area, attrs={'id': 'id-area'})
		output.append(s.render("area", selected_area))
		
		s = widgets.Select(choices=choices_room, attrs={'id': 'id-room'})
		output.append(s.render("room", selected_room))
		
		s = widgets.TextInput(attrs={'id': 'id-position'})
		output.append(s.render("pos", selected_pos))
		
		return(mark_safe('\n'.join(output)))	
	
	def value_from_datadict(self, data, files, name):
		from archive.models import Location
		(location, created) = Location.objects.get_or_create(area=data.get('area'), room=data.get('room'), position_ref=data.get('pos'))
		return(location.pk)
		#return([data.get('area'), data.get('room'), data.get('pos')])
			

class LocationWidget(widgets.MultiWidget):
	def __init__(self, attrs=None):
		from archive.models import Location
		_widgets = (
			widgets.Select(choices=[(l.area, l.area) for l in Location.objects.all()]),
			widgets.Select(attrs),
			widgets.TextInput(attrs)
		)
		super(LocationWidget, self).__init__(_widgets, attrs)
	
	def decompress(self, value):
		from archive.models import Location
		if value:
			l = Location.objects.get(pk=value)
			return([l.area, l.room, l.position_ref])
		return([None, None, None])


class MaterialWidget(widgets.Widget):
	def render(self, name, value, attrs=None):
		from archive.models import Materials
		final_attrs = self.build_attrs(attrs, type='text', name=name)
		objects = []
		
		if value:	
			for each in value:
				try:
					tag = Materials.objects.get(pk=each)
					objects.append(tag)
				except:
					continue
			
			values = []
			for each in objects:
				values.append(str(each))
			value = ','.join(values)
			
			if value:
				final_attrs['value'] = value
		else:
			final_attrs['value'] = ''
		return mark_safe(u'<input%s />' % flatatt(final_attrs))

class KeywordWidget(widgets.Widget):
	def render(self, name, value, attrs=None):
		from archive.models import Keywords
		final_attrs = self.build_attrs(attrs, type='text', name=name)
		objects = []
		
		if value:	
			for each in value:
				try:
					tag = Keywords.objects.get(pk=each)
					objects.append(tag)
				except:
					continue
			
			values = []
			for each in objects:
				values.append(str(each))
			value = ','.join(values)
			
			if value:
				final_attrs['value'] = value
		else:
			final_attrs['value'] = ''
		return mark_safe(u'<input%s />' % flatatt(final_attrs))

class TagWidget(widgets.Widget):
	def render(self, name, value, attrs=None):
		final_attrs = self.build_attrs(attrs, type='text', name=name)
		objects = []
		
		if value:	
			for each in value:
				try:
					tag = Tag.objects.get(pk=each)
					objects.append(tag)
				except:
					continue
			
			values = []
			for each in objects:
				values.append(str(each))
			value = ','.join(values)
			
			if value:
				final_attrs['value'] = value
		else:
			final_attrs['value'] = ''
		return mark_safe(u'<input%s />' % flatatt(final_attrs))
