from django.contrib import admin
from django import forms
from django.conf.urls import patterns
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.forms.widgets import Select, HiddenInput
from django.db import models 
from django.utils.translation import ugettext_lazy as _

from archive.models import Item, Tag, Media, Location, Condition, Category, Materials, Keywords, Address, Area, Room, Location, ItemMedia, File
from forms import ItemAdminForm, ItemSearchForm
from filters import ItemFilter

import pdb
import mimetypes

#Category.objects.all().annotate(cnt=Count('item')).exclude(cnt=0)

class ItemCategoryInline(admin.TabularInline):
	model=Item.category.through
	extra = 1
	template = 'admin/archive/edit_inline/category_tabular.html'

class MediaInline(admin.TabularInline):
	model=Item.media.through
	extra = 0
	template = 'admin/archive/edit_inline/media_tabular.html'
	ordering = ['order']
	fields = ['media', 'order']
		
	formfield_overrides = {
		models.ForeignKey: {'widget': HiddenInput},
	}
	
	class Media:
		js = ('js/jquery-1.8.2.min.js', 'js/jquery-ui-1.9.1.custom.min.js', 'js/media_inline.js', 'js/jquery.ui.touch-punch.min.js')

class FileInline(admin.TabularInline):
	model=File
	extra = 1

#--- Main Item Admin 
class ItemAdmin(admin.ModelAdmin):
	model = Item
	form = ItemAdminForm
	inlines = [MediaInline, ItemCategoryInline]	
	exclude = ('media', 'category')
	radio_fields = {'condition': admin.HORIZONTAL}
	search_fields = ['item_number', 'title', 'artist', 'materials__name', 'keywords__name', 'description', 'category__name']
	list_display = ['published', 'item_number', 'title', 'artist']
	actions = ['publish', 'unpublish']
	list_display_links = ['item_number']
	save_on_top = True
		
	fieldsets = (
			(None, { 'fields': ('published','item_number','title','condition', 'condition_comment')}),
			(_('Dating'), {'fields': ('dating_certainty', ('era_from', 'date_from', 'era_to', 'date_to'))
				}),
			(_('Origin'), {'fields': ('origin_certainty', ('origin_city', 'origin_country', 'origin_continent'), 'origin_provinience')
				}),
			(None, {'fields': ('artist',)
				}),
			(_('Dimensions'), {'fields': (('dim_height', 'dim_width', 'dim_depth', 'dim_weight'),)
				}),
			(_('Placement'), {'fields': (('address', 'area', 'room', 'location'), 'position')}), 
			(None, {'fields': ('materials', 'keywords', 'ref_literature', 'loan_status', 'description', 'insurance_value')}),
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
	
	def search(self, request):
		f = ItemFilter(request.POST, queryset=Item.objects.all())
		
		#if request.method == 'POST' and len(request.POST) > 0:
		#	redirect_url = '/admin/archive/item/?'
		#	for field in request.POST.lists():
		#		if field[1][0] and '_choices' not in field[0] and field[0] != 'csrfmiddlewaretoken':
		#			if not redirect_url[-1] == '?':
		#				redirect_url = redirect_url + '&'
		#			
		#			redirect_url = redirect_url + field[0]
		#			
		#			if request.POST.get(field[0] + '_choices') and request.POST.get(field[0] + '_choices') != 'EQ':
		#				redirect_url = redirect_url + '__' + request.POST.get(field[0] + '_choices').lower()
		#			
		#			redirect_url = redirect_url + '=' + field[1][0]
		#	return HttpResponseRedirect(redirect_url)	
		page_items = {}
		page_items['search_form'] = ItemSearchForm()
		page_items['filter'] = f
		return render_to_response('archive/search.html', page_items, context_instance=RequestContext(request))
		
#---

class CategoryAdmin(admin.ModelAdmin):
	model = Category

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
	inlines = [FileInline]	
	#exclude = ('files', )

admin.site.register(File)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Media, MediaAdmin)
admin.site.register(Condition)
admin.site.register(Item, ItemAdmin)
admin.site.register(Address)
admin.site.register(Area)
admin.site.register(Room)
admin.site.register(Location)
