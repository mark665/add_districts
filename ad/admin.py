from django.contrib import admin
from ad.models import Congress_Districts, Version

class VersionAdmin(admin.ModelAdmin):
  list_display = (
		  'name',
		  'pub',
		  'pub_url',
		  'date_valid',
		  'date_invalid',
		  'source_url',
		  'date_addded',
		 )

class CongressAdmin(admin.ModelAdmin):
  list_display = (
		  'state_fips',
		  'cd_fips',
		  'geo_id',
		  'name',
		  'cd_session',
		 )

admin.site.register(Congress_Districts,CongressAdmin)
admin.site.register(Version,VersionAdmin)
