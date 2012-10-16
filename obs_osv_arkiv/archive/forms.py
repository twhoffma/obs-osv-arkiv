import pdb
from django import forms
from django.forms import widgets
from archive.models import Item, Topic, Condition, Tag, Location, Keywords, Materials
from archive.widgets import TopicWidget, TagWidget, SelectLocationWidget, KeywordWidget, MaterialWidget
from archive.fields import TopicField, LocationField

from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from itertools import chain

class ItemSearchForm(forms.Form):
	item_number = forms.CharField() 
	title = forms.CharField() 
	

class ItemAdminForm(forms.ModelForm):
	materials = forms.CharField(widget=MaterialWidget(), required=False)
	keywords = forms.CharField(widget=KeywordWidget(), required=False)
		
	class Meta:
		model = Item
	
	def __init__(self, *args, **kwargs):
		super(ItemAdminForm, self).__init__(*args, **kwargs)
		self.fields['location'].widget = SelectLocationWidget()
	
	def clean(self):
		self.cleaned_data = super(ItemAdminForm, self).clean()
		#lookup and link materials
		materials = []
		keywords = []
		for material in self.cleaned_data['materials'].split(','):
			try:
				(m, created) = Materials.objects.get_or_create(name=material)
				materials.append(m)
			except:
				continue
		
		for keyword in self.cleaned_data['keywords'].split(','):
			try:
				(k, created) = Keywords.objects.get_or_create(name=keyword)
				keywords.append(k)
			except:
				continue
		
		self.cleaned_data['materials'] = materials
		self.cleaned_data['keywords'] = keywords
		#
		#for k in ['materials', 'keywords']:
		#	tags = []
		#	for material in self.cleaned_data[k].split(','):
		#		try:
		#			t = Tag.objects.get(name=material)
		#			tags.append(t)
		#		except:
		#			continue
		#	self.cleaned_data[k] = tags
		return(self.cleaned_data)

class Item_materialEditForm(forms.ModelForm):
	class Meta:
		model = Item.materials.through
		widgets = {'tag': TagWidget}
	


#class Item_topicEditForm(forms.ModelForm):
#	topic = TopicField(required=False)
#	
#	class Meta:
#		model = Item.topic.through
#		widgets = {'topic': TopicWidget(attrs={})}
#	
#	def clean(self):
#		self.cleaned_data = super(Item_topicEditForm, self).clean()
#		
#		return(self.cleaned_data)
#	
#class TopicEditForm(forms.ModelForm):
#	class Meta:
#		model = Topic
#		fields = (
#			'topic',
#			'subtopic'
#		)
#		widgets = {
#			'topic': forms.TextInput(attrs={'class': 'dobbel'}),
#			'subtopic': forms.TextInput(attrs={'class': 'dobbel'}),
#		}
#		
#		def __init__(self, *args, **kwargs):
#			super(TopicEditForm, self).__init__(*args, **kwargs)
#			self.fields['topic'].widget.attrs['class'] = 'dobbel'
#			self.fields['subtopic'].widget.attrs['class'] = 'dobbel'

class LocationEditForm(forms.ModelForm):
	class Meta:
		model = Location

class LocationSelectForm(forms.Form):
	area = forms.ChoiceField(choices=[(l.area, l.area) for l in Location.objects.all()])
	room = forms.ChoiceField(choices=[])
	position_ref = forms.ChoiceField(choices=[])
	
	def __init(self, *args, **kwargs):
		super

class TopicSelectForm(forms.Form):
	topic = forms.ChoiceField(choices=[], label=None)
	subtopic = forms.ChoiceField(choices=[], label=None)
	
	def __init__(self, *args, **kwargs):
		super(TopicSelectForm, self).__init__(*args, **kwargs)
		self.fields['topic'].widget.attrs.update({'class': 'dobbel'})
		self.fields['subtopic'].widget.attrs.update({'class': 'dobbel'})
		self.fields['topic'].choices = [t.topic for t in Topic.objects.all()]
		
	
class ItemEditForm(forms.ModelForm):
	condition = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=Condition.objects.all(), empty_label=None)
	materials = forms.CharField(required=False, widget=widgets.TextInput(attrs={'class' : 'material enkel'}))
	keywords = forms.CharField(required=False, widget=widgets.TextInput(attrs={'class': 'keyword enkel'}))
	
	class Meta:
		model = Item
		fields = (
			'item_number',
			'title',
			'condition',
			'dating_certainty',
			'era_from',
			'date_from',
			'era_to',
			'date_to',
			'origin_certainty',
			'origin_city',
			'origin_country',
			'origin_continent',
			'artist',
			'dim_height',
			'dim_width',
			'dim_depth',
			'dim_weight',
			'ref_literature',
			'aquization_method',
			'location',
			'loan_status',
			'description'
		)
		widgets = {
			'item_number': forms.TextInput(attrs={'class': 'enkel'}),
			'title': forms.TextInput(attrs={'class': 'enkel'}),
			'condition': forms.RadioSelect,
			'date_from': forms.TextInput(attrs={'class': 'dobbel'}),
			'date_to': forms.TextInput(attrs={'class': 'dobbel'}),
			'origin_city': forms.TextInput(attrs={'class': 'trippel'}),
			'origin_country': forms.TextInput(attrs={'class': 'trippel'}),
			'origin_continent': forms.TextInput(attrs={'class': 'trippel'}),
			'artist': forms.TextInput(attrs={'class': 'enkel'}),
			'dim_height': forms.TextInput(attrs={'class': 'dobbel'}),
			'dim_width': forms.TextInput(attrs={'class': 'dobbel'}),
			'dim_depth': forms.TextInput(attrs={'class': 'dobbel'}),
			'dim_weight': forms.TextInput(attrs={'class': 'dobbel'}),
			'ref_literatur': forms.TextInput(attrs={'class': 'dobbel'}),
			'aquization_method': forms.Textarea(attrs={'class': 'enkel'}),
			'loan_status': forms.TextInput(attrs={'class': 'enkel'}),
			'description': forms.Textarea(attrs={'cols': 80, 'rows': 20, 'class': 'enkel'}),
		}
