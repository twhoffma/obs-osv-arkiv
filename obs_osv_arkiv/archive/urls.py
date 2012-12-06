from django.conf.urls import patterns, include, url
import archive

urlpatterns = patterns('',
    url(r'^$', archive.views.ItemListView.as_view()), 
    url(r'^node/(?P<node_pk>\d+)/$', archive.views.ItemListView.as_view(), name='node'), 
    url(r'^node/(?P<node_pk>\d+)/item/(?P<pk>\d+)$', archive.views.ItemDetailView.as_view(), name='node_and_item'), 
    url(r'^item/(?P<pk>\d+)/$', archive.views.ItemDetailView.as_view(), name='item'), 
    url(r'^country/(?P<country>.*)/$', archive.views.ItemListView.as_view(), name='country'), 
    url(r'^artist/(?P<artist>.*)/$', archive.views.ItemListView.as_view(), name='artist'), 
    url(r'^city/(?P<city>.*)/$', archive.views.ItemListView.as_view(), name='city'), 
    url(r'^tag_autocomplete/$', 'archive.views.tag_autocomplete'),
    url(r'^keyword_autocomplete/$', 'archive.views.keyword_autocomplete'),
    url(r'^material_autocomplete/$', 'archive.views.material_autocomplete'),
    url(r'^room_autocomplete/$', 'archive.views.room_autocomplete'),
    url(r'^area_autocomplete/$', 'archive.views.area_autocomplete'),
    url(r'^location_autocomplete/$', 'archive.views.location_autocomplete'),
    url(r'^media_details/$', 'archive.views.image_details'),
    url(r'^search_autocomplete/$', 'archive.views.search_autocomplete'),
)
