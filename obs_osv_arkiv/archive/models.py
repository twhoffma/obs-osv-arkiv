#coding=utf-8

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class Category(MPTTModel):
	name = models.CharField(max_length=50)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
	
	class Meta:
		unique_together = (("name", "parent"), )
	
	def __unicode__(self):
		category_path = [c.name for c in self.get_ancestors()]
		category_path.append(self.name)
		return('>'.join(category_path))	

class Media(models.Model):
	MEDIA_TYPES = (
		('Image', 'Digital image'),
		('Movie', 'Digital movie'),
		('Sound', 'Digital sound'),
		('Text', 'Digital text (e.g. pdf)')
	)
	filename = models.FileField(upload_to='media')
	media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
	
	def __unicode__(self):
		return(self.filename.name)
	
#XXX: This should change. either unique=False or separate models for each field. Maybe put area, room and position in Item?
#class Location(models.Model):
#	area = models.CharField(max_length=100)
#	room = models.CharField(max_length=100)
#	position_ref = models.CharField(max_length=200)
#	
#	def __unicode__(self):
#		return(self.area + "," + self.room + "," + self.position_ref)

class Tag(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200, blank=True, null=True)
	
	def __unicode__(self):
		return(self.name)

class Materials(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200, blank=True, null=True)
	
	def __unicode__(self):
		return(self.name)

class Keywords(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200, blank=True, null=True)
	
	def __unicode__(self):
		return(self.name)

class Condition(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=300)
	condition_value = models.IntegerField(max_length=3)
	
	def __unicode__(self):
		return str(self.condition_value)

class Topic(models.Model):
	topic = models.CharField(max_length=200)
	subtopic = models.CharField(max_length=200, blank=True, null=True)
	
	def __unicode__(self):
		return(self.topic)

class Address(models.Model):
	name = models.CharField(max_length=200)
	street = models.CharField(max_length=200, blank=True, null=True)
	postal_number = models.CharField(max_length=200, blank=True, null=True)
	postal_area = models.CharField(max_length=200, blank=True, null=True)
	country = models.CharField(max_length=200, blank=True, null=True)
	
	def __unicode__(self):
		return(self.name)

class Area(models.Model):
	name = models.CharField(max_length=200) 
	address = models.ForeignKey(Address)
	
	class Meta:
		unique_together = (("name", "address"), )
	
	def __unicode__(self):
		return(self.name)

class Room(models.Model):
	name = models.CharField(max_length=200)
	area = models.ForeignKey(Area)
	
	class Meta:
		unique_together = (("name", "area"), )
	
	def __unicode__(self):
		return(self.name)

class Location(models.Model):
	name = models.CharField(max_length=200)
	room = models.ForeignKey(Room)
	
	class Meta:
		unique_together = (("name", "room"), )
	
	def __unicode__(self):
		return(self.name)

class Item(models.Model):
	ERA_CHOICES = (
		('BC', 'Before Christ'),
		('AD', 'Anno Domini')
	)
	CERTAINTY_CHOICES = (
		('Certain', 'Certain'),
		('Uncertain', 'Approximate or uncertain')
	)
	published = models.BooleanField()
	feature_media = models.ForeignKey(Media, verbose_name=u'Feature Media', blank=True, null=True, related_name='feature_media_set')
	item_number = models.CharField(max_length=14, unique=True, blank=False, verbose_name=u'Identifikasjonsnummer')
	title = models.CharField(max_length=200, blank=True, verbose_name=u'Tittel/Betegnelse', null=True)
	condition = models.ForeignKey(Condition, blank=True, null=True, verbose_name=u'Tilstand')
	dating_certainty = models.CharField(max_length=20, choices=CERTAINTY_CHOICES, verbose_name=u'Sikkerhet', blank=True, null=True) 
	era_from = models.CharField(max_length=2, choices=ERA_CHOICES, verbose_name=u'Periode', blank=True, null=True)
	date_from = models.IntegerField(verbose_name=u'Fra', blank=True, null=True)
	era_to = models.CharField(max_length=2, choices=ERA_CHOICES, verbose_name=u'Periode', blank=True, null=True)
	date_to = models.IntegerField(verbose_name=u'Til', blank=True, null=True)
	origin_certainty = models.CharField(max_length=20, choices=CERTAINTY_CHOICES, verbose_name=u'Sikkerhet', blank=True, null=True) 
	origin_city = models.CharField(max_length=200, verbose_name=u'By', blank=True, null=True)
	origin_country = models.CharField(max_length=200, verbose_name=u'Land', blank=True, null=True)
	origin_continent = models.CharField(max_length=200, verbose_name=u'Verdensdel', blank=True, null=True)
	artist = models.CharField(max_length=200, verbose_name=u'Kunstner/Produsent', blank=True, null=True)
	dim_height = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=u'Høyde (cm)', blank=True, null=True)
	dim_width = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=u'Bredde (cm)', blank=True, null=True)
	dim_depth = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=u'Dybde (cm)', blank=True, null=True)
	dim_weight = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=u'Vekt (g)', blank=True, null=True)
	materials = models.ManyToManyField(Materials, verbose_name=u'Materiale/Teknikk', blank=True)
	keywords = models.ManyToManyField(Keywords, verbose_name=u'Nøkkelord', blank=True)
	ref_literature = models.TextField(verbose_name=u'Ref. Litteratur', blank=True)	
	aquization_method = models.CharField(max_length=200, verbose_name=u'Proviniens', blank=True, null=True)
	address = models.ForeignKey(Address, verbose_name=u'Sted', blank=True, null=True)
	area = models.ForeignKey(Area, verbose_name=u'Område', blank=True, null=True)
	room = models.ForeignKey(Room, verbose_name=u'Rom', blank=True, null=True)
	location = models.ForeignKey(Location, verbose_name=u'Lokasjon', blank=True, null=True)	
	position = models.CharField(max_length=200, blank=True, null=True)
	loan_status = models.CharField(max_length=200, verbose_name=u'Utlånsstatus', blank=True, null=True)
	description = models.CharField(max_length=2000, verbose_name=u'Supplerende', blank=True, null=True)
	media = models.ManyToManyField(Media, verbose_name=u'Media', blank=True)
	category = models.ManyToManyField(Category, blank=True, null=True)
	#qr_archive = models.ImageField()
	#qr_exhibit = models.ImageField()	
	
	def __unicode__(self):
		return(self.item_number)

