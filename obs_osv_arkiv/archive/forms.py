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

class ItemAdminListFilterForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('address', 'area', 'room', 'location')

class ItemSearchForm(forms.Form):
	TEXT_CHOICES = (('ICONTAINS',_('contains')), ('ISTARTSWITH',_('starts with')), ('IENDSWITH', _('ends with')))
	NUMBER_CHOICES = (('GTE',_('>=')), ('LTE', _('<=')), ('EQ', _('=')))
	DATE_CHOICES = (('GTE',_('>=')), ('LTE', _('<=')), ('EQ', _('=')))
	
	published = forms.BooleanField(label=_("published"))
	item_number_choices = forms.ChoiceField(choices=TEXT_CHOICES)
	item_number = forms.CharField(label=_("item number")) 
	title_choices = forms.ChoiceField(choices=TEXT_CHOICES)
	title = forms.CharField(label=_("title")) 
	condition = forms.ModelChoiceField(queryset=Condition.objects.all(), label=_("condition"), widget=forms.RadioSelect)
	condition_comment = forms.CharField(label=_('condition details'))
	
	dim_height_choices = forms.ChoiceField(choices=NUMBER_CHOICES)
	dim_height = forms.DecimalField(decimal_places=2, max_digits=9, label=_("height (cm)"))
	dim_width_choices = forms.ChoiceField(choices=NUMBER_CHOICES)
	dim_width = forms.DecimalField(decimal_places=2, max_digits=9, label=_("width (cm)"))
	dim_depth_choices = forms.ChoiceField(choices=NUMBER_CHOICES)
	dim_depth = forms.DecimalField(decimal_places=2, max_digits=9, label=_("depth (cm)"))
	dim_weight_choices = forms.ChoiceField(choices=NUMBER_CHOICES)
	dim_weight = forms.DecimalField(decimal_places=2, max_digits=9, label=_("weight (g)"))
	
	#dating_certainty = models.CharField(max_length=20, choices=CERTAINTY_CHOICES, verbose_name=_("certainty"), blank=True, null=True) 
	#era_from = models.CharField(max_length=2, choices=ERA_CHOICES, verbose_name=_("period"), blank=True, null=True)
	#date_from = models.IntegerField(verbose_name=_("from"), blank=True, null=True)
	#era_to = models.CharField(max_length=2, choices=ERA_CHOICES, verbose_name=_("period"), blank=True, null=True)
	#date_to = models.IntegerField(verbose_name=_("to"), blank=True, null=True)
	#origin_certainty = models.CharField(max_length=20, choices=CERTAINTY_CHOICES, verbose_name=_("certainty"), blank=True, null=True) 
	#origin_city = models.CharField(max_length=200, verbose_name=_("city"), blank=True, null=True)
	#origin_country = models.CharField(max_length=200, verbose_name=_("country"), blank=True, null=True)
	#origin_continent = models.CharField(max_length=200, verbose_name=_("continent"), blank=True, null=True)
	#origin_provinience = models.TextField(verbose_name=_("provinience"), blank=True, null=True)
	#artist = models.CharField(max_length=200, verbose_name=_("artist"), blank=True, null=True)
	#dim_height = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_("height (cm)"), blank=True, null=True)
	#dim_width = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_("width (cm)"), blank=True, null=True)
	#dim_depth = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_("depth (cm)"), blank=True, null=True)
	#dim_weight = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_("weight (g)"), blank=True, null=True)
	#materials = models.ManyToManyField(Materials, verbose_name=_("materials/technique"), blank=True)
	#keywords = models.ManyToManyField(Keywords, verbose_name=_("keywords"), blank=True)
	#ref_literature = models.TextField(verbose_name=_("literature"), blank=True)	
	#address = models.ForeignKey(Address, verbose_name=_("address"), blank=True, null=True)
	#area = models.ForeignKey(Area, verbose_name=_("area"), blank=True, null=True)
	#room = models.ForeignKey(Room, verbose_name=_("room"), blank=True, null=True)
	#location = models.ForeignKey(Location, verbose_name=_("location"), blank=True, null=True)	
	#position = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("position"))
	#loan_status = models.CharField(max_length=200, verbose_name=_("loan status"), blank=True, null=True)
	#description = models.TextField(verbose_name=_("description"), blank=True, null=True)
	#media = models.ManyToManyField(Media, verbose_name=_("media"), blank=True, through=ItemMedia)
	#category = models.ManyToManyField(Category, blank=True, null=True, verbose_name=_("categories"))
	#insurance_value = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_('insurance value'), blank=True, null=True)
	
class ItemAdminForm(forms.ModelForm):
	materials = forms.CharField(widget=ManyToManyTextWidget(attrs={'rows': 3, 'cls': Materials}), required=False, label=_("Materials"))
	keywords = forms.CharField(widget=ManyToManyTextWidget(attrs={'rows': 3, 'cls': Keywords}), required=False, label=_("Keywords"))
		
	class Meta:
		model = Item
	
	def __init__(self, *args, **kwargs):
		super(ItemAdminForm, self).__init__(*args, **kwargs)
	
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
