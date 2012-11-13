from django.contrib import admin
from django import forms
from django.conf.urls import patterns
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from archive.models import Item, Topic, Tag, Media, Location, Condition, Category, Materials, Keywords
from forms import Item_materialEditForm, ItemAdminForm, ItemSearchForm
import pdb
import mimetypes

import autocomplete_light

class ItemCategoryInline(admin.TabularInline):
	model=Item.category.through
	extra = 0

class MaterialsInline(admin.TabularInline):
	model=Item.materials.through
	extra = 0
	form = Item_materialEditForm

class MediaInline(admin.TabularInline):
	model=Item.media.through
	extra = 1
	template = 'admin/archive/edit_inline/media_tabular.html'

#class AddressAdmin(admin.ModelAdmin):
#	model = 

class ItemAdmin(admin.ModelAdmin):
	model = Item
	form = ItemAdminForm
	inlines = [MediaInline, ItemCategoryInline]	
	exclude = ('media', 'category')
	radio_fields = {'condition': admin.HORIZONTAL}	
	fieldsets = (
			(None, { 'fields': (
				'published',
				'feature_media',
				'item_number',
				'title',
				'condition',
				)
				}),
			('Datering', {'fields': ('dating_certainty', 'era_from', 'date_from', 'era_to', 'date_to')
				}),
			('Lokasjon', {'fields': ('origin_certainty', 'origin_city', 'origin_country', 'origin_continent')
				}),
			(None, {'fields': ('artist',)
				}),
			('Dimensions', {'fields': ('dim_height', 'dim_width', 'dim_depth', 'dim_weight')
				}),
			('Sted', {'fields': ('address', 'area', 'room', 'location', 'position')}), 
			(None, {'fields': ('materials', 'keywords', 'ref_literature', 'aquization_method', 'loan_status', 'description')}),
		)
	
	def get_urls(self):
		urls = super(ItemAdmin, self).get_urls()
		extra_urls = patterns('',
			(r'^search/$', self.admin_site.admin_view(self.search))
		)
		return(extra_urls+urls)
	
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
		#page_items['search_form'] = ItemAdminForm()
		page_items['search_form'] = ItemSearchForm()
		return render_to_response('archive/search.html', page_items, context_instance=RequestContext(request))

class CategoryAdmin(admin.ModelAdmin):
	form = autocomplete_light.modelform_factory(Category)

class MediaAdmin(admin.ModelAdmin):
	model = Media
	
	def save_model(self, request, obj, form, change):
		from PIL import Image
		from django.conf import settings
		import re
		
		#Guess filetype
		(mimetype, submimetype) = mimetypes.guess_type(obj.filename.name)
		is_image = not re.match('image/.*', mimetype) is None
		
		obj.save()
		file = settings.MEDIA_ROOT + "/" + obj.filename.name
		
		if is_image:
			im = Image.open(file)
			im.thumbnail((50,50), Image.ANTIALIAS)
			matches = re.split('(.*)\.([^\.]*)$', file)
			im.save(matches[1] + "_thumb.jpg" , "JPEG")
	
admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic)
admin.site.register(Tag)
admin.site.register(Media, MediaAdmin)
admin.site.register(Location)
admin.site.register(Condition)
admin.site.register(Item, ItemAdmin)
