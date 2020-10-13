#coding=utf-8

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from os.path import split, splitext
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer

import os
import settings


class ItemHistory(models.Model):
	action_time = models.DateTimeField(_('action time'), auto_now=True) 
	user = models.ForeignKey(User)
	item = models.ForeignKey('Item')
	field = models.CharField(max_length=50, verbose_name=_("field"))
	value = models.CharField(max_length=200, verbose_name=_("value"))

class Category(MPTTModel):
	name = models.CharField(max_length=50, verbose_name=_("name"))
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_("parent"))
	description = models.TextField(null=True, blank=True)
	
	class Meta:
		unique_together = (("name", "parent"), )
		verbose_name = _("category")
		verbose_name_plural = _("categories")
	
	def __unicode__(self):
		category_path = [c.name for c in self.get_ancestors()]
		category_path.append(self.name)
		return('>'.join(category_path))

class File(models.Model):
	file = models.FileField(upload_to='media', verbose_name=_("file"))
	media = models.ForeignKey('Media')
	order = models.IntegerField(blank=True, null=True)	
	
	class Meta:
		verbose_name = _("file")
		verbose_name_plural = _("files")
	
	def content_type(self):
		import mimetypes
		type = mimetypes.guess_type(self.file.name)[0]
		if type is None: #Should include a test for webm
			type = 'video/webm'
		return(type)
	
	def __unicode__(self):
		return(self.file.name)
	
class Media(models.Model):
	MEDIA_TYPE_IMAGE = 'Picture'
	MEDIA_TYPE_MOVIE = 'Movie'
	MEDIA_TYPE_SOUND = 'Sound'
	MEDIA_TYPE_TEXT = 'Text'
	MEDIA_TYPE_MISC = 'Misc'

	MEDIA_TYPES = (
		(MEDIA_TYPE_IMAGE, _("Picture")),
		(MEDIA_TYPE_MOVIE, _('Film/Animation')),
		(MEDIA_TYPE_SOUND, _('Sound')),
		(MEDIA_TYPE_TEXT, _('Text')),
		(MEDIA_TYPE_MISC, _('Other'))
	)

	ICON_COLOR_BLACK = 0
	ICON_COLOR_WHITE = 1
	ICON_COLORS = (
		(ICON_COLOR_WHITE, _("White")),
		(ICON_COLOR_BLACK, _("Black")),
	)
	
	filename = models.FileField(upload_to='media', verbose_name=_("thumbnail"), blank=True)
	media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, verbose_name=_("filetype"))
	macro_zoom = models.BooleanField(default=False)
	icon_color = models.IntegerField(default=ICON_COLOR_WHITE, choices=ICON_COLORS)
	
	class Meta:
		verbose_name = _("media")
		verbose_name_plural = _("media")
	
	def icon_color_name(self):
		if self.icon_color == self.ICON_COLOR_BLACK:
			return 'black'
		return 'white'

	def thumbnail(self, width, height):
		"""
		Generate a thumbnail image of this media file, and return its URL.
		"""
		if self.filename and os.path.exists(self.filename.path):
			thumbnailer = get_thumbnailer(self.filename)
			try:
				thumb = thumbnailer.get_thumbnail({'size': (width, height)})
				thumb_url = thumb.url
				return thumb_url
			except:
				pass

		thumb_url = settings.STATIC_URL + 'images/'
		
		if self.media_type == self.MEDIA_TYPE_IMAGE:
			thumb_url = thumb_url + 'thumb_image.jpg'
		elif self.media_type == self.MEDIA_TYPE_MOVIE:
			thumb_url = thumb_url + 'thumb_movie.jpg'
		elif self.media_type == self.MEDIA_TYPE_SOUND:
			thumb_url = thumb_url + 'thumb_audio.jpg'
		elif self.media_type == self.MEDIA_TYPE_TEXT:
			thumb_url = thumb_url + 'thumb_text.jpg'
		else:
			thumb_url = thumb_url + 'thumb_misc.jpg'
		return(thumb_url)
		
	def __unicode__(self):
		from os.path import basename
		if self.filename:
			if self.file_set.all().count() > 0:
				if self.file_set.all().count() > 2:
					return(basename(self.filename.name) + u' (' + unicode(self.file_set.all().count()) + u' ' + 'files' + ')')
				else:
					return(basename(self.filename.name) + ' (' + ', '.join([basename(f.file.name) for f in self.file_set.all()]) + ')')
			else:
				return(basename(self.filename.name))
		elif self.file_set.count() > 0:
			return(basename(self.file_set.all()[0].file.name))
		else:
			return(_('media') + u' ' + str(self.pk))

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
		('sure', _("sure")),
		('uncertain', _("approximate/uncertain"))
	)

	class Meta:
		verbose_name = _('Item')
		verbose_name_plural = _('Items')
	
	def header_image(self):
		return(self.itemmedia_set.order_by('order')[:1])
		
	published = models.BooleanField(verbose_name=_("published"), default=False)
	item_number = models.CharField(max_length=14, unique=True, blank=False, verbose_name=_("item number"))
	title = models.CharField(max_length=200, blank=True, verbose_name=_("title"), null=True)
	condition = models.ForeignKey(Condition, blank=True, null=True, verbose_name=_("condition"))
	condition_comment = models.TextField(verbose_name=_('condition details'), blank=True, null=True)
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
	insurance_value = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_('insurance value'), blank=True, null=True)
	
	def __unicode__(self):
		return(self.item_number)


# vi: se noet:
