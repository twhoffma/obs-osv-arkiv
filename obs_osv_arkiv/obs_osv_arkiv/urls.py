from django.conf.urls import patterns, include, url
from django.conf import settings
from archive import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import archive

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'obs_osv_arkiv.views.home', name='home'),
    # url(r'^obs_osv_arkiv/', include('obs_osv_arkiv.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('', include('archive.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

