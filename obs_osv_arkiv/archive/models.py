#coding=utf-8

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class Category(MPTTModel):
	name = models.CharField(max_length=50)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
	
	class Meta:
		unique_together = (("name", "parent"), )
		verbose_name = "Kategori"
		verbose_name_plural = "Kategorier"
	
	def __unicode__(self):
		category_path = [c.name for c in self.get_ancestors()]
		category_path.append(self.name)
		return('>'.join(category_path))	

class Media(models.Model):
	MEDIA_TYPES = (
		('Image', 'Bilde'),
		('Movie', 'Film/Animasjon'),
		('Sound', 'Lyd'),
		('Text', 'Tekst'),
		('Misc', 'Annen')
	)
	filename = models.FileField(upload_to='media')
	media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
	
	class Meta:
		verbose_name = "Medie"
		verbose_name_plural = "Medier"
		
	def __unicode__(self):
		return(self.filename.name)
	
class Tag(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200, blank=True, null=True)
	
	class Meta:
		verbose_name = "Tag"
		verbose_name_plural = "Tagger"
		
	def __unicode__(self):
		return(self.name)

class Materials(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200, blank=True, null=True)
	
	class Meta:
		verbose_name = "Materiale"
		verbose_name_plural = "Materialer"
	
	def __unicode__(self):
		return(self.name)

class Keywords(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200, blank=True, null=True)
	
	class Meta:
		verbose_name = "Nøkkelord"
		verbose_name_plural = "Nøkkelord"
	
	def __unicode__(self):
		return(self.name)

class Condition(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=300)
	condition_value = models.IntegerField(max_length=3)
	
	class Meta:
		verbose_name = "Tilstand"
		verbose_name_plural = "Tilstander"
	
	def __unicode__(self):
		return str(self.condition_value)

class Topic(models.Model):
	topic = models.CharField(max_length=200)
	subtopic = models.CharField(max_length=200, blank=True, null=True)
	
	class Meta:
		verbose_name = "Materiale"
		verbose_name_plural = "Materialer"
	
	def __unicode__(self):
		return(self.topic)

class Address(models.Model):
	name = models.CharField(max_length=200)
	street = models.CharField(max_length=200, blank=True, null=True)
	postal_number = models.CharField(max_length=200, blank=True, null=True)
	postal_area = models.CharField(max_length=200, blank=True, null=True)
	country = models.CharField(max_length=200, blank=True, null=True)
	
	class Meta:
		verbose_name = "Addresse"
		verbose_name_plural = "Addresser"
	
	def __unicode__(self):
		return(self.name)

class Area(models.Model):
	name = models.CharField(max_length=200) 
	address = models.ForeignKey(Address)
	
	class Meta:
		unique_together = (("name", "address"), )
		verbose_name = "Område/Bygning"
		verbose_name_plural = "Områder/Bygninger"
	
	def __unicode__(self):
		return(self.name)

class Room(models.Model):
	name = models.CharField(max_length=200)
	area = models.ForeignKey(Area)
	
	class Meta:
		unique_together = (("name", "area"), )
		verbose_name = "Underområde/Rom"
		verbose_name_plural = "Underområder/Rom"
	
	def __unicode__(self):
		return(self.name)

class Location(models.Model):
	name = models.CharField(max_length=200)
	room = models.ForeignKey(Room)
	
	class Meta:
		unique_together = (("name", "room"), )
		verbose_name = "Sted"
		verbose_name_plural = "Steder"
	
	def __unicode__(self):
		return(self.name)

class Item(models.Model):
	ERA_CHOICES = (
		('FVT', 'Før vår tid'),
		('EVT', 'Etter vår tid')
	)
	CERTAINTY_CHOICES = (
		('Sikker', 'Sikker'),
		('Usikker', 'Tilnærmet eller usikker')
	)

	class Meta:
		verbose_name = u'Gjenstand'
		verbose_name_plural = u'Gjenstander'
	
	published = models.BooleanField()
	feature_media = models.ForeignKey(Media, verbose_name=u'Hovedbilde', blank=True, null=True, related_name='feature_media_set')
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
	origin_provinience = models.TextField(verbose_name=u'Proveniens', blank=True, null=True)
	artist = models.CharField(max_length=200, verbose_name=u'Kunstner/Produsent', blank=True, null=True)
	dim_height = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=u'Høyde (cm)', blank=True, null=True)
	dim_width = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=u'Bredde (cm)', blank=True, null=True)
	dim_depth = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=u'Dybde (cm)', blank=True, null=True)
	dim_weight = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=u'Vekt (g)', blank=True, null=True)
	materials = models.ManyToManyField(Materials, verbose_name=u'Materiale/Teknikk', blank=True)
	keywords = models.ManyToManyField(Keywords, verbose_name=u'Nøkkelord', blank=True)
	ref_literature = models.TextField(verbose_name=u'Ref. Litteratur', blank=True)	
	address = models.ForeignKey(Address, verbose_name=u'Sted', blank=True, null=True)
	area = models.ForeignKey(Area, verbose_name=u'Område', blank=True, null=True)
	room = models.ForeignKey(Room, verbose_name=u'Rom', blank=True, null=True)
	location = models.ForeignKey(Location, verbose_name=u'Lokasjon', blank=True, null=True)	
	position = models.CharField(max_length=200, blank=True, null=True)
	loan_status = models.CharField(max_length=200, verbose_name=u'Utlånsstatus', blank=True, null=True)
	description = models.TextField(verbose_name=u'Supplerende', blank=True, null=True)
	media = models.ManyToManyField(Media, verbose_name=u'Media', blank=True)
	category = models.ManyToManyField(Category, blank=True, null=True)
	#qr_archive = models.ImageField()
	#qr_exhibit = models.ImageField()	
	
	def __unicode__(self):
		return(self.item_number)

