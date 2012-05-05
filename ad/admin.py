from django.contrib import admin
from ad.models import Congress_Districts

class CongressAdmin(admin.ModelAdmin):
  list_display = (
		  'state_fips',
		  'cd_fips',
		  'geo_id',
		  'name',
		  'cd_session',
		 )

admin.site.register(Congress_Districts,CongressAdmin)
