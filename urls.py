from django.conf import settings
from django.conf.urls.defaults import * 
from django.views.generic.simple import direct_to_template
# Use geogjango admin
from django.contrib.gis import admin

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'ad.views.home', name='home'),
    url(r'^index.json$', 'ad.views.results_geojson'),

    url(r'^processed$', 'ad.views.processed_files'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),

    url(r'^.*media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

