from django.contrib import admin
from django import forms
from django.conf.urls import patterns
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from archive.models import Item, Tag, Media, Location, Condition, Category, Materials, Keywords, Address, Area, Room, Location #,Topic
from django.core.urlresolvers import reverse
from forms import Item_materialEditForm, ItemAdminForm, ItemSearchForm
import autocomplete_light
import pdb
import mimetypes
from django.forms.widgets import Select
from django.db import models 
from django.utils.translation import ugettext_lazy as _

class ItemCategoryInline(admin.TabularInline):
	model=Item.category.through
	extra = 0

class MediaInline(admin.TabularInline):
	model=Item.media.through
	extra = 0
	template = 'admin/archive/edit_inline/media_tabular.html'
	ordering = ['order']
	fields = ['media', 'order']
	
	class Media:
		js = ('js/jquery-ui-1.9.1.custom.min.js', )

#--- Main Item Admin 
class ItemAdmin(admin.ModelAdmin):
	model = Item
	form = ItemAdminForm
	inlines = [MediaInline, ItemCategoryInline]	
	exclude = ('media', 'category')
	radio_fields = {'condition': admin.HORIZONTAL}
	search_fields = ['item_number', 'title', 'artist', 'materials__name', 'keywords__name', 'description']
	list_display = ['published', 'item_number', 'title', 'artist']
	actions = ['publish', 'unpublish']
	list_display_links = ['item_number']
	save_on_top = True
	
	fieldsets = (
			(None, { 'fields': ('published','feature_media','item_number','title','condition')}),
			(_('Dating'), {'fields': ('dating_certainty', ('era_from', 'date_from', 'era_to', 'date_to'))
				}),
			('Lokasjon', {'fields': ('origin_certainty', ('origin_city', 'origin_country', 'origin_continent'), 'origin_provinience')
				}),
			(None, {'fields': ('artist',)
				}),
			(_('Dimensions'), {'fields': (('dim_height', 'dim_width', 'dim_depth', 'dim_weight'),)
				}),
			(_('Placement'), {'fields': (('address', 'area', 'room', 'location'), 'position')}), 
			(None, {'fields': ('materials', 'keywords', 'ref_literature', 'loan_status', 'description')}),
		)
	
	def get_urls(self):
		urls = super(ItemAdmin, self).get_urls()
		extra_urls = patterns('',
			(r'^search/$', self.admin_site.admin_view(self.search)),
			#(r'^adv_search/$', self.admin_site.admin_view(self.adv_search)),
		)
		return(extra_urls+urls)

	def publish(self, request, queryset):
		for obj in queryset:
			obj.published = True
			obj.save()
	
	def unpublish(self, request, queryset):
		for obj in queryset:
			obj.published = False
			obj.save()
	
	#def search(self, request):
	#	redirect_url = '/admin/archive/item/'
	#	
	#	if request.method == 'GET' and len(request.GET) > 0:
	#		redirect_url = redirect_url + '?'
	#		query = request.GET['query']
	#		if query:
	#			redirect_url = redirect_url + 'title__icontains=' + query
	#	return HttpResponseRedirect(redirect_url)
	
	def search(self, request):
		if request.method == 'GET' and len(request.GET) > 0:
			redirect_url = '/admin/archive/item/?'
			for field in request.GET.lists():
				if field[1][0]:
					if not redirect_url[-1] == '?':
						redirect_url = redirect_url + '&'
					redirect_url = redirect_url + field[0] + '__icontains=' + field[1][0]
			return HttpResponseRedirect(redirect_url)	
		page_items = {}
		page_items['search_form'] = ItemSearchForm()
		return render_to_response('archive/search.html', page_items, context_instance=RequestContext(request))
		
#---

#--- Category Admin for organization
class CategoryAdmin(admin.ModelAdmin):
	form = autocomplete_light.modelform_factory(Category)

#---

#---Item location admin interfaces
class AddressAdmin(admin.ModelAdmin):
	model = Address

class AreaAdmin(admin.ModelAdmin):
	model = Area

class RoomAdmin(admin.ModelAdmin):
	model = Room

class LocationAdmin(admin.ModelAdmin):
	model = Location
#---

#--- File and media admins
class MediaAdmin(admin.ModelAdmin):
	model = Media
	
	def save_model(self, request, obj, form, change):
		#from PIL import Image
		from django.conf import settings
		import re
		
		#Guess filetype
		(mimetype, submimetype) = mimetypes.guess_type(obj.filename.name)
		#is_image = not re.match('image/.*', mimetype) is None
		
		obj.save()
		file = settings.MEDIA_ROOT + "/" + obj.filename.name
		
		i#f is_image:
		#	im = Image.open(file)
		#	im.thumbnail((50,50), Image.ANTIALIAS)
		#	matches = re.split('(.*)\.([^\.]*)$', file)
		#	im.save(matches[1] + "_thumb.jpg" , "JPEG")
#
#---

admin.site.register(Category, CategoryAdmin)
#admin.site.register(Topic)
admin.site.register(Tag)
admin.site.register(Media, MediaAdmin)
admin.site.register(Condition)
admin.site.register(Item, ItemAdmin)
admin.site.register(Address)
admin.site.register(Area)
admin.site.register(Room)
admin.site.register(Location)
