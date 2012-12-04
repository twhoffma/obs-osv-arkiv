#coding=utf-8

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Category(MPTTModel):
	name = models.CharField(max_length=50, verbose_name=_("name"))
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_("parent"))
	
	class Meta:
		unique_together = (("name", "parent"), )
		verbose_name = _("category")
		verbose_name_plural = _("categories")
	
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
	filename = models.FileField(upload_to='media', verbose_name=_("filename"))
	media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, verbose_name=_("filetype"))
	
	class Meta:
		verbose_name = _("media")
		verbose_name_plural = _("media")
		
	def __unicode__(self):
		return(self.filename.name)

class ItemMedia(models.Model):
	item = models.ForeignKey('Item', verbose_name=_("item"))
	media = models.ForeignKey('Media', verbose_name=_("media"))
	order = models.IntegerField(verbose_name=_("order"))
	
	def __unicode__(self):
		return(self.media.__unicode__())
	
class Tag(models.Model):
	name = models.CharField(max_length=200, verbose_name=_("name"))
	description = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("description"))
	
	class Meta:
		verbose_name = _("tag")
		verbose_name_plural = _("tags")
		
	def __unicode__(self):
		return(self.name)

class Materials(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200, blank=True, null=True)
	
	class Meta:
		verbose_name = _("material")
		verbose_name_plural = _("materials")
	
	def __unicode__(self):
		return(self.name)

class Keywords(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200, blank=True, null=True)
	
	class Meta:
		verbose_name = _("keywords")
		verbose_name_plural = _("keywords")
	
	def __unicode__(self):
		return(self.name)

class Condition(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=300)
	condition_value = models.IntegerField(max_length=3)
	
	class Meta:
		verbose_name = _("condition")
		verbose_name_plural = _("conditions")
	
	def __unicode__(self):
		return str(self.condition_value)

class Address(models.Model):
	name = models.CharField(max_length=200, verbose_name=_("name"))
	street = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("street"))
	postal_number = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("postal number"))
	postal_area = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("postal area"))
	country = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("country"))
	
	class Meta:
		verbose_name = _("address")
		verbose_name_plural = _("addresses")
	
	def __unicode__(self):
		return(self.name)

class Area(models.Model):
	name = models.CharField(max_length=200, verbose_name=_("name")) 
	address = models.ForeignKey(Address, verbose_name=_("address"))
	
	class Meta:
		unique_together = (("name", "address"), )
		verbose_name = _("area/building")
		verbose_name_plural = _("areas/buildings")
	
	def __unicode__(self):
		return(self.name)

class Room(models.Model):
	name = models.CharField(max_length=200, verbose_name=_("name"))
	area = models.ForeignKey(Area, verbose_name=_("area"))
	
	class Meta:
		unique_together = (("name", "area"), )
		verbose_name = _("subarea/room")
		verbose_name_plural = _("subareas/rooms")
	
	def __unicode__(self):
		return(self.name)

class Location(models.Model):
	name = models.CharField(max_length=200, verbose_name=_("name"))
	room = models.ForeignKey(Room, verbose_name=_("room"))
	
	class Meta:
		unique_together = (("name", "room"), )
		verbose_name = _("location")
		verbose_name_plural = _("locations")
	
	def __unicode__(self):
		return(self.name)

class Item(models.Model):
	ERA_CHOICES = (
		('AD', _('AD')),
		('BC', _('BC'))
	)
	CERTAINTY_CHOICES = (
		('sure', _('sure')),
		('uncertain', _('approximate/uncertain'))
	)

	class Meta:
		verbose_name = _('Item')
		verbose_name_plural = _('Items')
	
	def header_image(self):
		return(self.itemmedia_set.order_by('order')[:1])
		
	published = models.BooleanField(verbose_name=_("published"))
	feature_media = models.ForeignKey(Media, verbose_name=_("feature image"), blank=True, null=True, related_name='feature_media_set')
	item_number = models.CharField(max_length=14, unique=True, blank=False, verbose_name=_("item number"))
	title = models.CharField(max_length=200, blank=True, verbose_name=_("title"), null=True)
	condition = models.ForeignKey(Condition, blank=True, null=True, verbose_name=_("condition"))
	dating_certainty = models.CharField(max_length=20, choices=CERTAINTY_CHOICES, verbose_name=_("certainty"), blank=True, null=True) 
	era_from = models.CharField(max_length=2, choices=ERA_CHOICES, verbose_name=_("period"), blank=True, null=True)
	date_from = models.IntegerField(verbose_name=_("from"), blank=True, null=True)
	era_to = models.CharField(max_length=2, choices=ERA_CHOICES, verbose_name=_("period"), blank=True, null=True)
	date_to = models.IntegerField(verbose_name=_("to"), blank=True, null=True)
	origin_certainty = models.CharField(max_length=20, choices=CERTAINTY_CHOICES, verbose_name=_("certainty"), blank=True, null=True) 
	origin_city = models.CharField(max_length=200, verbose_name=_("city"), blank=True, null=True)
	origin_country = models.CharField(max_length=200, verbose_name=_("country"), blank=True, null=True)
	origin_continent = models.CharField(max_length=200, verbose_name=_("continent"), blank=True, null=True)
	origin_provinience = models.TextField(verbose_name=_("provinience"), blank=True, null=True)
	artist = models.CharField(max_length=200, verbose_name=_("artist"), blank=True, null=True)
	dim_height = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_("height (cm)"), blank=True, null=True)
	dim_width = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_("width (cm)"), blank=True, null=True)
	dim_depth = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_("depth (cm)"), blank=True, null=True)
	dim_weight = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_("weight (g)"), blank=True, null=True)
	materials = models.ManyToManyField(Materials, verbose_name=_("materials/technique"), blank=True)
	keywords = models.ManyToManyField(Keywords, verbose_name=_("keywords"), blank=True)
	ref_literature = models.TextField(verbose_name=_("literature"), blank=True)	
	address = models.ForeignKey(Address, verbose_name=_("address"), blank=True, null=True)
	area = models.ForeignKey(Area, verbose_name=_("area"), blank=True, null=True)
	room = models.ForeignKey(Room, verbose_name=_("room"), blank=True, null=True)
	location = models.ForeignKey(Location, verbose_name=_("location"), blank=True, null=True)	
	position = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("position"))
	loan_status = models.CharField(max_length=200, verbose_name=_("loan status"), blank=True, null=True)
	description = models.TextField(verbose_name=_("description"), blank=True, null=True)
	media = models.ManyToManyField(Media, verbose_name=_("media"), blank=True, through=ItemMedia)
	category = models.ManyToManyField(Category, blank=True, null=True, verbose_name=_("categories"))
	#qr_archive = models.ImageField()
	#qr_exhibit = models.ImageField()	
	
	def __unicode__(self):
		return(self.item_number)

