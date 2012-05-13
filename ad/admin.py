from django.contrib import admin
from django.contrib.gis import admin
from ad.models import Congress_Districts, Counties, States, Blocks

admin.site.register(States, admin.OSMGeoAdmin)
admin.site.register(Counties, admin.OSMGeoAdmin)
admin.site.register(Congress_Districts, admin.OSMGeoAdmin)
admin.site.register(Blocks, admin.OSMGeoAdmin)
