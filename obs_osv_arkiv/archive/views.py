from archive.models import Media, Tag, Condition, Item, Category, Address, Area, Room, Location, Materials
from django.shortcuts import render_to_response, get_object_or_404
from archive.forms import ItemSearchForm
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.template import Template, RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from haystack.query import SearchQuerySet

from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormView

import json

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

class ItemSearchResultView(ItemListView):

	def get(self, request):
		frm = ItemSearchForm(request.GET)
		self.object_list = Item.objects.none()

		if frm.is_valid():

			cdata = frm.clean()
			sqs = SearchQuerySet().filter(published=True)
			psqs = sqs

			# No blank values, please
			for key in cdata.iterkeys():
				if isinstance(cdata[key], basestring):
					cdata[key] = cdata[key].strip()

			if cdata['categories']:
				sqs = sqs.filter(categories__in=[x.strip() for x in cdata['categories'].split(' ')])
			if cdata['title']:
				sqs = sqs.filter(title=cdata['title'])
			if cdata['artist']:
				sqs = sqs.filter(artist=cdata['artist'])
			if cdata['date_from']:
				sqs = sqs.filter(date_from__gte=cdata['date_from'])
			if cdata['date_to']:
				sqs = sqs.filter(date_to__lte=cdata['date_to'])
			if cdata['origin_city']:
				sqs = sqs.filter(origin_city=cdata['origin_city'])
			if cdata['origin_country']:
				sqs = sqs.filter(origin_country=cdata['origin_country'])
			if cdata['materials']:
				sqs = sqs.filter(materials__in=[x.strip() for x in cdata['materials'].split(' ')])
			if cdata['video_only']:
				sqs = sqs.filter(video_only=True)

			# fulltext search
			if cdata['q']:
				sqs = sqs.filter(content=cdata['q'])

			# No search data entered
			if psqs == sqs:
				return redirect(reverse('item_search'))

			# Assigning a list to self.object_list won't work, it needs a QuerySet.
			# We're basically loading the items twice :(
			results = list(sqs.order_by('score')[:1000])  # slicing the array prevents multiple queries to Solr.
			ids = [x.object.id for x in results]  # sqs.values_list('django_id', flat=True) won't work with Haystack.
			self.object_list = Item.objects.filter(id__in=ids)

		self.parent_category = None
		self.current_category = None
		self.child_categories = None
		context = self.get_context_data(object_list=self.object_list)
		return(self.render_to_response(context))	

	def get_context_data(self, **kwargs):
		context = super(ItemSearchResultView, self).get_context_data(**kwargs)
		context['bg'] = None
		context['search'] = True
		return context

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

# vi: se noet:
