#coding=utf-8

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Category(MPTTModel):
	name = models.CharField(max_length=50)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
	
	class Meta:
		unique_together = (("name", "parent"), )
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")
	
	def __unicode__(self):
		category_path = [c.name for c in self.get_ancestors()]
		category_path.append(self.name)
		return('>'.join(category_path))

class Media(models.Model):
	MEDIA_TYPES = (
		('Image', _("Picture")),
		('Movie', _('Film/Animation')),
		('Sound', _('Sound')),
		('Text', _('Text')),
		('Misc', _('Other'))
	)
	filename = models.FileField(upload_to='media')
	media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
	
	class Meta:
		verbose_name = _("Media")
		verbose_name_plural = _("Media")
		
	def __unicode__(self):
		return(self.filename.name)

class ItemMedia(models.Model):
	item = models.ForeignKey('Item')
	media = models.ForeignKey('Media')
	order = models.IntegerField()
	
	def __unicode__(self):
		return(self.media.__unicode__())
	
class Tag(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200, blank=True, null=True)
	
	class Meta:
		verbose_name = _("Tag")
		verbose_name_plural = _("Tags")
		
	def __unicode__(self):
		return(self.name)

class Materials(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200, blank=True, null=True)
	
	class Meta:
		verbose_name = _("Material")
		verbose_name_plural = _("Materialer")
	
	def __unicode__(self):
		return(self.name)

class Keywords(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200, blank=True, null=True)
	
	class Meta:
		verbose_name = _("Keywords")
		verbose_name_plural = _("Keywords")
	
	def __unicode__(self):
		return(self.name)

class Condition(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=300)
	condition_value = models.IntegerField(max_length=3)
	
	class Meta:
		verbose_name = _("Condition")
		verbose_name_plural = _("Conditions")
	
	def __unicode__(self):
		return str(self.condition_value)

#class Topic(models.Model):
#	topic = models.CharField(max_length=200)
#	subtopic = models.CharField(max_length=200, blank=True, null=True)
#	
#	class Meta:
#		verbose_name = "Material"
#		verbose_name_plural = "Materialer"
#	
#	def __unicode__(self):
#		return(self.topic)

class Address(models.Model):
	name = models.CharField(max_length=200)
	street = models.CharField(max_length=200, blank=True, null=True)
	postal_number = models.CharField(max_length=200, blank=True, null=True)
	postal_area = models.CharField(max_length=200, blank=True, null=True)
	country = models.CharField(max_length=200, blank=True, null=True)
	
	class Meta:
		verbose_name = _("Address")
		verbose_name_plural = _("Addresses")
	
	def __unicode__(self):
		return(self.name)

class Area(models.Model):
	name = models.CharField(max_length=200) 
	address = models.ForeignKey(Address)
	
	class Meta:
		unique_together = (("name", "address"), )
		verbose_name = _("Area/Building")
		verbose_name_plural = _("Areas/Buildings")
	
	def __unicode__(self):
		return(self.name)

class Room(models.Model):
	name = models.CharField(max_length=200)
	area = models.ForeignKey(Area)
	
	class Meta:
		unique_together = (("name", "area"), )
		verbose_name = _("Subarea/Room")
		verbose_name_plural = _("Subareas/Rooms")
	
	def __unicode__(self):
		return(self.name)

class Location(models.Model):
	name = models.CharField(max_length=200)
	room = models.ForeignKey(Room)
	
	class Meta:
		unique_together = (("name", "room"), )
		verbose_name = _("Location")
		verbose_name_plural = _("Locations")
	
	def __unicode__(self):
		return(self.name)

class Item(models.Model):
	ERA_CHOICES = (
		('AD', _('AD')),
		('BC', _('BC'))
	)
	CERTAINTY_CHOICES = (
		('Sikker', _('Sure')),
		('Usikker', _('Approximate/Uncertain'))
	)

	class Meta:
		verbose_name = _('Item')
		verbose_name_plural = _('Items')
	
	published = models.BooleanField()
	feature_media = models.ForeignKey(Media, verbose_name=_('Feature image'), blank=True, null=True, related_name='feature_media_set')
	item_number = models.CharField(max_length=14, unique=True, blank=False, verbose_name=_('Item number'))
	title = models.CharField(max_length=200, blank=True, verbose_name=_('Title'), null=True)
	condition = models.ForeignKey(Condition, blank=True, null=True, verbose_name=_('Condition'))
	dating_certainty = models.CharField(max_length=20, choices=CERTAINTY_CHOICES, verbose_name=_('Certainty'), blank=True, null=True) 
	era_from = models.CharField(max_length=2, choices=ERA_CHOICES, verbose_name=_('Period'), blank=True, null=True)
	date_from = models.IntegerField(verbose_name=_('From'), blank=True, null=True)
	era_to = models.CharField(max_length=2, choices=ERA_CHOICES, verbose_name=_('Period'), blank=True, null=True)
	date_to = models.IntegerField(verbose_name=_('To'), blank=True, null=True)
	origin_certainty = models.CharField(max_length=20, choices=CERTAINTY_CHOICES, verbose_name=_('Certainty'), blank=True, null=True) 
	origin_city = models.CharField(max_length=200, verbose_name=_('City'), blank=True, null=True)
	origin_country = models.CharField(max_length=200, verbose_name=_('Country'), blank=True, null=True)
	origin_continent = models.CharField(max_length=200, verbose_name=_('Continent'), blank=True, null=True)
	origin_provinience = models.TextField(verbose_name=_('Provinience'), blank=True, null=True)
	artist = models.CharField(max_length=200, verbose_name=_('Artist'), blank=True, null=True)
	dim_height = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_('Height (cm)'), blank=True, null=True)
	dim_width = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_('Width (cm)'), blank=True, null=True)
	dim_depth = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_('Depth (cm)'), blank=True, null=True)
	dim_weight = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_('Weight (g)'), blank=True, null=True)
	materials = models.ManyToManyField(Materials, verbose_name=_('Materials/Technique'), blank=True)
	keywords = models.ManyToManyField(Keywords, verbose_name=_('Keywords'), blank=True)
	ref_literature = models.TextField(verbose_name=_('Literature'), blank=True)	
	address = models.ForeignKey(Address, verbose_name=_('Address'), blank=True, null=True)
	area = models.ForeignKey(Area, verbose_name=_('Area'), blank=True, null=True)
	room = models.ForeignKey(Room, verbose_name=_('Room'), blank=True, null=True)
	location = models.ForeignKey(Location, verbose_name=_('Location'), blank=True, null=True)	
	position = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Position'))
	loan_status = models.CharField(max_length=200, verbose_name=_('Loan status'), blank=True, null=True)
	description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
	media = models.ManyToManyField(Media, verbose_name=_('Media'), blank=True, through=ItemMedia)
	category = models.ManyToManyField(Category, blank=True, null=True, verbose_name=_('Categories'))
	#qr_archive = models.ImageField()
	#qr_exhibit = models.ImageField()	
	
	def __unicode__(self):
		return(self.item_number)

