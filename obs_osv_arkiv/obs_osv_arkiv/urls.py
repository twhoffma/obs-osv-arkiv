from django.conf.urls import patterns, include, url
from django.conf import settings
from archive import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'obs_osv_arkiv.views.home', name='home'),
    # url(r'^obs_osv_arkiv/', include('obs_osv_arkiv.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'archive.views.museum'),
    url(r'^admin/search/', 'archive.views.search'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^add_location/$', 'archive.views.add_location'),
    url(r'^tag_autocomplete/$', 'archive.views.tag_autocomplete'),
    url(r'^keyword_autocomplete/$', 'archive.views.keyword_autocomplete'),
    url(r'^material_autocomplete/$', 'archive.views.material_autocomplete'),
    url(r'^topic_autocomplete/$', 'archive.views.topic_autocomplete'),
    url(r'^subtopic_autocomplete/$', 'archive.views.subtopic_autocomplete'),
    url(r'^room_autocomplete/$', 'archive.views.room_autocomplete'),
    (r'%s(?P<path>.*)' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^navigation/', include('navigation_autocomplete.urls')),
)
