from archive.models import Media, Tag, Condition, Item, Category, Address, Area, Room, Location, Materials
from django.shortcuts import render_to_response, get_object_or_404
from archive.forms import ItemSearchForm
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf
#from django.forms.formsets import formset_factory
#from django.forms.models import modelformset_factory, inlineformset_factory
from django.utils import simplejson
import json
from django.views.decorators.csrf import csrf_exempt
from django.template import Template, RequestContext
from django.core.urlresolvers import reverse

from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormView
import pdb

class ItemSearchView(FormView):
	template_name = 'archive/search.html'
	form_class = ItemSearchForm
	
class ItemListView(ListView):
	model = Item
	
	def get_queryset(self):
		if self.kwargs.get('node_pk'):
			c = get_object_or_404(Category, pk=self.kwargs.get('node_pk'))
			self.parent_category = c.get_ancestors().order_by('name')
			self.current_category = c
			self.child_categories = c.get_children().filter(pk__in=Item.category.through.objects.filter(item__published=True).values_list('category__pk', flat=True).distinct().filter(category__in=c.get_descendants(include_self=True))).order_by('name')
			return(c.item_set.filter(published=True))
		elif self.kwargs.get('country'):
			self.parent_category = None
			self.current_category = None
			self.child_categories = None
			return(Item.objects.filter(origin_country__iexact=self.kwargs.get('country')).filter(published=True))
		elif self.kwargs.get('artist'):
			self.parent_category = None
			self.current_category = None
			self.child_categories = None
			return(Item.objects.filter(artist__iexact=self.kwargs.get('artist')).filter(published=True))
		elif self.kwargs.get('city'):
			self.parent_category = None
			self.current_category = None
			self.child_categories = None
			return(Item.objects.filter(origin_city__iexact=self.kwargs.get('city')).filter(published=True))
		else:
			self.parent_category = None
			self.current_category = None
			#self.child_categories = Category.objects.root_nodes().filter(id__in=[m.category.get_root().pk for m in Item.category.through.objects.filter(item__published=True)]).order_by('name')
			self.child_categories = Category.objects.root_nodes().filter(tree_id__in=Item.category.through.objects.filter(item__published=True).values_list('category__tree_id').distinct()).order_by('name')
			return(Item.objects.filter(pk=None).filter(published=True))
	
	def post(self, request, *args, **kwargs):
		frm = ItemSearchForm(request.POST)
		self.object_list = Item.objects.filter(published=True)
		
		if frm.is_valid():
			cleaned_data = frm.clean()
			if cleaned_data['category']:
				self.object_list = self.object_list.filter(category__name__icontains=cleaned_data['category'])
			if cleaned_data['title']:
				self.object_list = self.object_list.filter(title__icontains=cleaned_data['title'])
			if cleaned_data['artist']:
				self.object_list = self.object_list.filter(artist__icontains=cleaned_data['artist'])
			if cleaned_data['date_from']:
				self.object_list = self.object_list.filter(date_from__gte=cleaned_data['date_from'])
			if cleaned_data['date_to']:
				self.object_list = self.object_list.filter(date_to__lte=cleaned_data['date_to'])
			if cleaned_data['city']:
				self.object_list = self.object_list.filter(origin_city__iexact=cleaned_data['date_to'])
			if cleaned_data['country']:
				self.object_list = self.object_list.filter(origin_country__iexact=cleaned_data['date_to'])
			if cleaned_data['material']:
				m = Materials.objects.filter(name__iexact=cleaned_data['material'])
				self.object_list = self.object_list.filter(materials__in=m)
			if cleaned_data['checkmovie']:
				pdb.set_trace()
				self.object_list = self.object_list.filter(media__media_type='Movie')
		self.parent_category = None
		self.current_category = None
		self.child_categories = None
		context = self.get_context_data(object_list=self.object_list)
		return(self.render_to_response(context))	
		
	
	def get_context_data(self, **kwargs):
		context = super(ItemListView, self).get_context_data(**kwargs)
		context['parent'] = self.parent_category
		context['current'] = self.current_category
		context['nodes'] = self.child_categories
		if self.object_list:
			context['bg'] = None
		elif (self.parent_category and self.parent_category.count > 0) or self.current_category:
			context['bg'] = u'flyvemann2.jpg'
		else:
			context['bg'] = u'flyvemann1.jpg'
		return(context)

class ItemDetailView(DetailView):
	model = Item
	
	def get_queryset(self):
		try:	
			i = Item.objects.filter(pk=self.kwargs.get('pk'))
		except Item.DoesNotExist:
			i = None
		
		try:
			c = Category.objects.get(pk=self.kwargs.get('node_pk'))
			self.current_category = c
			self.parent_category = c.get_ancestors().order_by('name')
		except Category.DoesNotExist:
			c = None
			self.current_category = None
			self.parent_category = None
		
		return(i)
	
	def get_context_data(self, **kwargs):
		context = super(ItemDetailView, self).get_context_data(**kwargs)
		context['parent'] = self.parent_category
		context['current'] = self.current_category
		context['bg'] = None
		
		return(context)

@csrf_exempt
def filter_media(request):
	context = {}
	m = Media.objects.all()
	if request.method == "GET" and request.GET.has_key("query"):
		q = request.GET.get("query")
		m = m.filter(filename__icontains=q)
	context['media'] = m
	return render_to_response('archive/filter_media.html', context,context_instance=RequestContext(request))

@csrf_exempt
def search_autocomplete(request):
	from archive.models import Item
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Item.objects.filter(title__icontains=value).filter(published=True)
			
			for t in models:
				results.append({'value': reverse('item', kwargs={'pk': t.pk}), 'label': t.title})
				#if t.category.all().count > 0:
				#	results.append({'value': reverse('node_and_item', kwargs={'node_pk': t.category.all()[0].pk, 'pk': t.pk}), 'label': t.title})
				#else:
				#	results.append({'value': reverse('item', kwargs={'pk': t.pk}), 'label': t.title})
	#json = simplejson.dumps(results)
	json_out = json.dumps(results)
	return HttpResponse(json_out)

@csrf_exempt
def image_details(request):
	if request.method == "GET":
		from archive.models import Media
		mpk = request.GET.get('media_pk') 
		m = Media.objects.get(pk=mpk)
		context = {}
		context['filename'] = m.filename.name 
		context['file'] = m.filename
		context['mime'] = m.media_type
		context['m'] = m
		return render_to_response('archive/media_details.html', context,context_instance=RequestContext(request))

@csrf_exempt
def area_autocomplete(request):
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			if value:
				addr = Address.objects.filter(pk=value)
				models = Area.objects.filter(address=addr)
				results = [(t.pk, t.name) for t in models]
	#json = simplejson.dumps(results)
	json_out = json.dumps(results)
	return HttpResponse(json_out)

@csrf_exempt
def room_autocomplete(request):
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			if value:
				area = Area.objects.get(pk=value)
				models = Room.objects.filter(area=area)
				results = [(t.pk, t.name) for t in models]
	#json = simplejson.dumps(results)
	json_out = json.dumps(results)
	return HttpResponse(json_out)

@csrf_exempt
def location_autocomplete(request):
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			if value:
				room = Room.objects.get(pk=value)
				models = Location.objects.filter(room=room)
				results = [(t.pk, t.name) for t in models]
	#json = simplejson.dumps(results)
	json_out = json.dumps(results)
	return HttpResponse(json_out)

@csrf_exempt
def keyword_autocomplete(request):
	from archive.models import Keywords
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Keywords.objects.filter(name__icontains=value)
			results = [t.name for t in models]
	json_out = json.dumps(results)
	return HttpResponse(json_out)

@csrf_exempt
def material_autocomplete(request):
	from archive.models import Materials
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Materials.objects.filter(name__icontains=value)
			results = [t.name for t in models]
	json_out = json.dumps(results)
	return HttpResponse(json_out)

@csrf_exempt
def title_autocomplete(request):
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Item.objects.filter(title__icontains=value)
			#results = models.values_list('title')
			results = [t.title for t in models]
	json_out = json.dumps(results)
	return HttpResponse(json_out)

@csrf_exempt
def artist_autocomplete(request):
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Item.objects.filter(artist__icontains=value)
			results = list(models.values_list('artist', flat=True).distinct())
	json_out = json.dumps(results)
	return HttpResponse(json_out)

@csrf_exempt
def city_autocomplete(request):
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Item.objects.filter(origin_city__icontains=value).order_by('origin_city')
			results = list(models.values_list('origin_city', flat=True).distinct())
	json_out = json.dumps(results)
	return HttpResponse(json_out)

@csrf_exempt
def country_autocomplete(request):
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Item.objects.filter(origin_country__icontains=value).order_by('origin_country')
			results = list(models.values_list('origin_country', flat=True).distinct())
	json_out = json.dumps(results)
	return HttpResponse(json_out)

@csrf_exempt
def materials_autocomplete(request):
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Materials.objects.filter(pk__in=Item.materials.through.objects.values_list('materials__pk', flat=True)).distinct().order_by('name')
			results = list(models.filter(name__icontains=value).values_list('name', flat=True).distinct())
	json_out = json.dumps(results)
	return HttpResponse(json_out)

@csrf_exempt
def category_autocomplete(request):
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Category.objects.filter(pk__in=Item.category.through.objects.filter(item__published=True).values_list('category__pk', flat=True).distinct()).order_by('name')
			results = list(models.filter(name__icontains=value).values_list('name', flat=True).distinct().order_by('name'))
	json_out = json.dumps(results)
	return HttpResponse(json_out)

def copyright(request):
    return render_to_response("archive/copyright.html", {}, RequestContext(request))
