from django.contrib.gis.db import models

class Version(models.Model):
	
  name = models.CharField(max_length=50)	
  pub = models.CharField(max_length=100)
  pub_url = models.CharField(max_length=200)
  date_valid = models.DateField()
  date_invalid = models.DateField()
  source_url = models.CharField(max_length=250)
  date_addded = models.DateField()

  def __unicode__(self):
  	return self.name

class Congress_Districts(models.Model):

  version = models.ForeignKey(Version)

  state_fips = models.CharField(max_length=2)
  cd_fips = models.CharField(max_length=2)
  geo_id = models.CharField(max_length=7)
  name = models.CharField(max_length=50)
  cd_session = models.CharField(max_length=3)

  mpoly = models.MultiPolygonField()
  objects = models.GeoManager()

  def __unicode__(self):
  	return self.name

