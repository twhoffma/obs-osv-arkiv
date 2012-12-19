from archive.models import Media, Tag, Condition,Item, Category, Address, Area, Room, Location #,Topic
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory, inlineformset_factory
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.template import Template, RequestContext
from django.core.urlresolvers import reverse

from django.views.generic.list import ListView
from django.views.generic import DetailView
import pdb


class ItemListView(ListView):
	model = Item
	
	def get_queryset(self):
		if self.kwargs.get('node_pk'):
			c = get_object_or_404(Category, pk=self.kwargs.get('node_pk'))
			self.parent_category = c.get_ancestors().order_by('name')
			self.current_category = c
			self.child_categories = c.get_children().filter(pk__in=Item.category.through.objects.filter(item__published=True).values_list('category__pk', flat=True).distinct().filter(category__in=c.get_descendants(include_self=True))).order_by('name')
			return(c.item_set.all())
		elif self.kwargs.get('country'):
			self.parent_category = None
			self.current_category = None
			self.child_categories = None
			return(Item.objects.filter(origin_country__iexact=self.kwargs.get('country')))
		elif self.kwargs.get('artist'):
			self.parent_category = None
			self.current_category = None
			self.child_categories = None
			return(Item.objects.filter(artist__iexact=self.kwargs.get('artist')))
		elif self.kwargs.get('city'):
			self.parent_category = None
			self.current_category = None
			self.child_categories = None
			return(Item.objects.filter(origin_city__iexact=self.kwargs.get('city')))
		else:
			self.parent_category = None
			self.current_category = None
			#self.child_categories = Category.objects.get_roots().filter(id__in=Item.category.through.objects.filter(item__published=True).values_list('category__pk', flat=True).distinct()).order_by('name')
			self.child_categories = Category.objects.root_nodes().filter(id__in=[m.category.get_root().pk for m in Item.category.through.objects.filter(item__published=True)]).order_by('name')
			return(Item.objects.filter(pk=None))
	
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
	json = simplejson.dumps(results)
	return HttpResponse(json)

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

#@csrf_exempt
#def search(request):
#	return render_to_response('archive/search.html', context_instance=RequestContext(request))
#
#
#
#@csrf_exempt
#def museum(request):
#	page_items = {}
#	if request.GET.has_key('node'):
#		node_id = request.GET.get('node')
#		c = Category.objects.get(pk=node_id)
#		page_items['parent'] = c
#		page_items['nodes'] = c.get_children()
#		page_items['items'] = c.item_set.all()
#	else:
#		page_items['nodes'] = Category.objects.root_nodes()
#		#No items since all items displayed must a connection to the chosen node.
#		
#	return render_to_response('archive/museum.html', page_items, context_instance=RequestContext(request))

#used
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
	json = simplejson.dumps(results)
	return HttpResponse(json)

#used
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
	json = simplejson.dumps(results)
	return HttpResponse(json)

#used
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
	json = simplejson.dumps(results)
	return HttpResponse(json)

#@csrf_exempt
#def tag_autocomplete(request):
#	results = []
#	if request.method == "POST":
#		if request.POST.has_key(u'query'):
#			value = request.POST.get(u'query')
#			models = Tag.objects.filter(name__icontains=value)
#			results = [t.name for t in models]
#	json = simplejson.dumps(results)
#	return HttpResponse(json) #, mimetype='application/json')

@csrf_exempt
def keyword_autocomplete(request):
	from archive.models import Keywords
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Keywords.objects.filter(name__icontains=value)
			results = [t.name for t in models]
	json = simplejson.dumps(results)
	return HttpResponse(json)

@csrf_exempt
def material_autocomplete(request):
	from archive.models import Materials
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Materials.objects.filter(name__icontains=value)
			results = [t.name for t in models]
	json = simplejson.dumps(results)
	return HttpResponse(json)

#@csrf_exempt
#def topic_autocomplete(request):
#	results = []
#	if request.method == "POST":
#		if request.POST.has_key(u'topic'):
#			value = request.POST.get(u'topic')
#			models = Topic.objects.filter(topic__icontains=value)
#			results = [t.topic for t in models]
#	json = simplejson.dumps(results)
#	return HttpResponse(json)
#
#
#@csrf_exempt
#def room_autocomplete(request):
#	results = []
#	if request.method == "POST":
#		if request.POST.has_key(u'area'):
#			value = request.POST.get(u'area')
#			models = Location.objects.filter(area__iexact=value)
#			results = [t.room for t in models]
#	json = simplejson.dumps(results)
#	return HttpResponse(json)
#
#@csrf_exempt
#def subtopic_autocomplete(request):
#	results = []
#	if request.method == "POST":
#		if request.POST.has_key(u'topic') and request.POST.has_key(u'subtopic'):
#			topic = request.POST.get(u'topic')
#			subtopic = request.POST.get(u'subtopic')
#			models = Topic.objects.filter(topic__iexact=topic).filter(subtopic__icontains=subtopic)
#			results = [t.subtopic for t in models]
#	json = simplejson.dumps(results)
#	return HttpResponse(json)
#
#def add_location(request):
#	response = HttpResponse()
#	response['Content-Type'] = 'application/json'
#	
#	if request.method == "POST":
#		form = LocationEditForm(request.POST)
#		if form.is_valid():
#			form.save()
#			
#			response.write(simplejson.dumps("OK"))
#		else:
#			response.write(simplejson.dumps("FAIL: " + "\n" + "\n".join(form.errors.keys())))
#	else:
#		response.write("Not a POST")
#		#return HttpResponse("FAIL")
#	
#	return(response)

