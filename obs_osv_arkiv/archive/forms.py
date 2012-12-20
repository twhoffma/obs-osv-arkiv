import pdb
from django import forms
from django.forms import widgets
from archive.models import Item, Condition, Tag, Location, Keywords, Materials
from archive.widgets import KeywordWidget, MaterialWidget, ManyToManyTextWidget

from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from itertools import chain
from django.utils.translation import ugettext_lazy as _


class ItemSearchForm(forms.Form):
	TEXT_CHOICES = (('ICONTAINS',_('contains')), ('ISTARTSWITH',_('starts with')), ('IENDSWITH', _('ends with')))
	NUMBER_CHOICES = (('GTE',_('greater than or equal')), ('LTE', _('less than or equal')), ('EQ', _('equals')))
	DATE_CHOICES = (('GTE',_('greater than or equal')), ('LTE', _('less than or equal')), ('EQ', _('equals')))
	item_number = forms.CharField() 
	item_number_choices = forms.ChoiceField(choices=TEXT_CHOICES)
	title = forms.CharField() 
	title_choices = forms.ChoiceField(choices=TEXT_CHOICES)
	
class ItemAdminForm(forms.ModelForm):
	#materials = forms.CharField(widget=MaterialWidget(attrs={'rows': 3}), required=False, label=_("Materials"))
	#keywords = forms.CharField(widget=KeywordWidget(attrs={'rows': 3}), required=False, label=_("Keywords"))
	materials = forms.CharField(widget=ManyToManyTextWidget(attrs={'rows': 3, 'cls': Materials}), required=False, label=_("Materials"))
	keywords = forms.CharField(widget=ManyToManyTextWidget(attrs={'rows': 3, 'cls': Keywords}), required=False, label=_("Keywords"))
		
	class Meta:
		model = Item
	
	def __init__(self, *args, **kwargs):
		super(ItemAdminForm, self).__init__(*args, **kwargs)
		#self.fields['location'].widget = SelectLocationWidget()
	
	def clean(self):
		self.cleaned_data = super(ItemAdminForm, self).clean()
		#lookup and link materials
		materials = []
		keywords = []
		for material in self.cleaned_data['materials'].split(','):
			if len(material.strip()) > 0:
				try:
					(m, created) = Materials.objects.get_or_create(name=material)
					materials.append(m)
				except:
					continue
		
		for keyword in self.cleaned_data['keywords'].split(','):
			if len(keyword.strip()) > 0:
				try:
					(k, created) = Keywords.objects.get_or_create(name=keyword)
					keywords.append(k)
				except:
					continue
		
		self.cleaned_data['materials'] = materials
		self.cleaned_data['keywords'] = keywords
		
		return(self.cleaned_data)

#class Item_materialEditForm(forms.ModelForm):
#	class Meta:
#		model = Item.materials.through
#		widgets = {'tag': TagWidget}
#	
#
#
#class Item_topicEditForm(forms.ModelForm)V:
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
#
#class LocationEditForm(forms.ModelForm):
#	class Meta:
#		model = Location
#
#class LocationSelectForm(forms.Form):
#	area = forms.ChoiceField(choices=[(l.area, l.area) for l in Location.objects.all()])
#	room = forms.ChoiceField(choices=[])
#	position_ref = forms.ChoiceField(choices=[])
#	
#	def __init(self, *args, **kwargs):
#		super
#
#class TopicSelectForm(forms.Form):
#	topic = forms.ChoiceField(choices=[], label=None)
#	subtopic = forms.ChoiceField(choices=[], label=None)
#	
#	def __init__(self, *args, **kwargs):
#		super(TopicSelectForm, self).__init__(*args, **kwargs)
#		self.fields['topic'].widget.attrs.update({'class': 'dobbel'})
#		self.fields['subtopic'].widget.attrs.update({'class': 'dobbel'})
#		self.fields['topic'].choices = [t.topic for t in Topic.objects.all()]
#		
#	
#class ItemEditForm(forms.ModelForm):
#	condition = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=Condition.objects.all(), empty_label=None)
#	materials = forms.CharField(required=False, widget=widgets.TextInput(attrs={'class' : 'material enkel'}))
#	keywords = forms.CharField(required=False, widget=widgets.TextInput(attrs={'class': 'keyword enkel'}))
#	
#	class Meta:
#		model = Item
#		fields = (
#			'item_number',
#			'title',
#			'condition',
#			'dating_certainty',
#			'era_from',
#			'date_from',
#			'era_to',
#			'date_to',
#			'origin_certainty',
#			'origin_city',
#			'origin_country',
#			'origin_continent',
#			'artist',
#			'dim_height',
#			'dim_width',
#			'dim_depth',
#			'dim_weight',
#			'ref_literature',
#			'aquization_method',
#			'location',
#			'loan_status',
#			'description'
#		)
#		widgets = {
#			'item_number': forms.TextInput(attrs={'class': 'enkel'}),
#			'title': forms.TextInput(attrs={'class': 'enkel'}),
#			'condition': forms.RadioSelect,
#			'date_from': forms.TextInput(attrs={'class': 'dobbel'}),
#			'date_to': forms.TextInput(attrs={'class': 'dobbel'}),
#			'origin_city': forms.TextInput(attrs={'class': 'trippel'}),
#			'origin_country': forms.TextInput(attrs={'class': 'trippel'}),
#			'origin_continent': forms.TextInput(attrs={'class': 'trippel'}),
#			'artist': forms.TextInput(attrs={'class': 'enkel'}),
#			'dim_height': forms.TextInput(attrs={'class': 'dobbel'}),
#			'dim_width': forms.TextInput(attrs={'class': 'dobbel'}),
#			'dim_depth': forms.TextInput(attrs={'class': 'dobbel'}),
#			'dim_weight': forms.TextInput(attrs={'class': 'dobbel'}),
#			'ref_literatur': forms.TextInput(attrs={'class': 'dobbel'}),
#			'aquization_method': forms.Textarea(attrs={'class': 'enkel'}),
#			'loan_status': forms.TextInput(attrs={'class': 'enkel'}),
#			'description': forms.Textarea(attrs={'cols': 80, 'rows': 20, 'class': 'enkel'}),
#		}
