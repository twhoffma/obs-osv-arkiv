from django.contrib import admin
from django import forms
from django.conf.urls import patterns
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.forms.widgets import Select, HiddenInput
from django.db import models 
from django.utils.translation import ugettext_lazy as _

from archive.models import Item, Tag, Media, Location, Condition, Category, Materials, Keywords, Address, Area, Room, Location, ItemMedia, File, ItemHistory
from forms import ItemAdminForm #, ItemSearchForm,ItemAdminListFilterForm
from django.contrib.admin import RelatedFieldListFilter, SimpleListFilter, FieldListFilter

import pdb
import mimetypes

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
			
class FilterLocation(RelatedFieldListFilter):
	template = "archive/location_filter.html"

class FilterFromDate(SimpleListFilter):
	template = "archive/year_filter.html"
	title = 'from_date'
	parameter_name = 'from_date'
	
	def lookups(self, request, model_admin):
		return((self.value(),self.value()),)
		
	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(date_from__gte=self.value())
		else:
			return queryset
	
class FilterToDate(SimpleListFilter):
	template = "archive/year_filter.html"
	title = 'to_date'
	parameter_name = 'to_date'
	
	def lookups(self, request, model_admin):
		return((self.value(),self.value()),)
		
	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(date_to__lte=self.value())
		else:
			return queryset
	
#--- Main Item Admin 
class ItemAdmin(admin.ModelAdmin):
	model = Item
	form = ItemAdminForm
	inlines = [MediaInline, ItemCategoryInline]	
	exclude = ('media', 'category')
	radio_fields = {'condition': admin.HORIZONTAL}
	search_fields = ['item_number', 'title', 'artist', 'materials__name', 'keywords__name', 'description', 'category__name',
        'condition_comment', 'origin_city', 'origin_country', 'origin_continent', 'origin_provinience', 'ref_literature', 'position', 'loan_status',
            ]
	list_display = ['published', 'item_number', 'title', 'artist']
	actions = ['publish', 'unpublish']
	list_display_links = ['item_number']
	save_on_top = True
	list_filter = (('address', FilterLocation), ('area', FilterLocation), ('room', FilterLocation), ('location', FilterLocation), ('category', FilterLocation),)
	
	fieldsets = (
			(None, { 'fields': ('published','item_number','title', 'condition', 'condition_comment')}),
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
			#(r'^change_history/$', self.admin_site.admin_view(self.change_history)),
    			(r'^(?P<item_pk>.*)/change_history/(?P<field>.*)$', self.admin_site.admin_view(self.change_history)), 
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
	
	def change_history(self, request, item_pk, field):
		page_items = {}
		if item_pk  and field:
			#f = request.GET.get('field')
			#item_pk = request.GET.get('item_pk')
			page_items['object'] = Item.objects.get(pk=item_pk)
			page_items['action_list'] = ItemHistory.objects.filter(field=field).filter(item__pk=item_pk).order_by('-action_time')
		return render_to_response('admin/archive/item/change_history.html', page_items, context_instance=RequestContext(request))
	
	def changelist_view(self, request, extra_context=None):
		extra_context = extra_context or {}
		#extra_context['filter'] = ItemFilter(request.POST, queryset=Item.objects.all())
		#extra_context['listfilter'] = ItemAdminListFilterForm(request.POST)
		#pdb.set_trace()
		return super(ItemAdmin, self).changelist_view(request, extra_context)
		
	def save_model(self, request, obj, form, change):
		super(ItemAdmin, self).save_model(request, obj, form, change)
		
		log = ItemHistory.objects.filter(item=obj).filter(field='loan_status').order_by('-action_time')	
		
		if 'loan_status' in form.changed_data:
			new_log = ItemHistory(user=request.user, item=obj, field='loan_status', value=obj.loan_status)
			new_log.save()
		

class CategoryAdmin(admin.ModelAdmin):
	model = Category

class AddressAdmin(admin.ModelAdmin):
	model = Address

class AreaAdmin(admin.ModelAdmin):
	model = Area

class RoomAdmin(admin.ModelAdmin):
	model = Room

class LocationAdmin(admin.ModelAdmin):
	model = Location

class MediaAdmin(admin.ModelAdmin):
	model = Media
	inlines = [FileInline]	
	search_fields = ['filename', 'file__file', 'pk']

class MaterialAdmin(admin.ModelAdmin):
	model = Materials
	search_fields = ['name']

class KeywordAdmin(admin.ModelAdmin):
	model = Keywords
	search_fields = ['name']

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
admin.site.register(Materials, MaterialAdmin)
admin.site.register(Keywords, KeywordAdmin)
