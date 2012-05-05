from django.contrib import admin
from django.contrib.gis import admin
from ad.models import Congress_Districts

admin.site.register(Congress_Districts, admin.OSMGeoAdmin)
