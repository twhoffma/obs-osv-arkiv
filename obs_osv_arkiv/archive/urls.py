from django.conf.urls import patterns, include, url
import archive

urlpatterns = patterns('',
    url(r'^node/(\d+)/$|^$', archive.views.ItemListView.as_view()), 
    url(r'^item/(?P<pk>\d+)/$', archive.views.ItemDetailView.as_view()), 
    url(r'^tag_autocomplete/$', 'archive.views.tag_autocomplete'),
    url(r'^keyword_autocomplete/$', 'archive.views.keyword_autocomplete'),
    url(r'^material_autocomplete/$', 'archive.views.material_autocomplete'),
    url(r'^room_autocomplete/$', 'archive.views.room_autocomplete'),
    url(r'^area_autocomplete/$', 'archive.views.area_autocomplete'),
    url(r'^location_autocomplete/$', 'archive.views.location_autocomplete'),
)
