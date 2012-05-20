from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Congress_Districts(models.Model):
  statefp = models.CharField(max_length=2)
  cd112fp = models.CharField(max_length=2)
  geoid = models.CharField(max_length=7)
  namelsad = models.CharField(max_length=41)
  lsad = models.CharField(max_length=2)
  cdsessn = models.CharField(max_length=3)
  mtfcc = models.CharField(max_length=5)   
  funcstat = models.CharField(max_length=1)
  aland = models.FloatField()
  awater = models.FloatField()
  intptlat = models.CharField(max_length=11)
  intptlon = models.CharField(max_length=12)
  geom = models.MultiPolygonField(srid=4326)
  objects = models.GeoManager()

  def __unicode__(self):
    return self.namelsad

class Counties(models.Model):
  statefp10 = models.CharField(max_length=2)
  countyfp10 = models.CharField(max_length=3)
  countyns10 = models.CharField(max_length=8)
  geoid10 = models.CharField(max_length=5)
  name10 = models.CharField(max_length=100)
  namelsad10 = models.CharField(max_length=100)
  lsad10 = models.CharField(max_length=2)
  classfp10 = models.CharField(max_length=2)
  mtfcc10 = models.CharField(max_length=5)
  csafp10 = models.CharField(max_length=3)
  cbsafp10 = models.CharField(max_length=5)
  metdivfp10 = models.CharField(max_length=5)
  funcstat10 = models.CharField(max_length=1)
  aland10 = models.FloatField()
  awater10 = models.FloatField()
  intptlat10 = models.CharField(max_length=11)
  intptlon10 = models.CharField(max_length=12)
  geom = models.MultiPolygonField(srid=4326)
  objects = models.GeoManager()

  def __unicode__(self):
    return self.namelsad10

class States(models.Model):
  region = models.CharField(max_length=2)
  division = models.CharField(max_length=2)
  statefp = models.CharField(max_length=2)
  statens = models.CharField(max_length=8)
  geoid = models.CharField(max_length=2)
  stusps = models.CharField(max_length=2)
  name = models.CharField(max_length=100)
  lsad = models.CharField(max_length=2)
  mtfcc = models.CharField(max_length=5)
  funcstat = models.CharField(max_length=1)
  aland = models.FloatField()
  awater = models.FloatField()
  intptlat = models.CharField(max_length=11)
  intptlon = models.CharField(max_length=12)
  geom = models.MultiPolygonField(srid=4326)
  objects = models.GeoManager()

class Blocks(models.Model):
  statefp = models.CharField(max_length=2)
  countyfp = models.CharField(max_length=3)
  statefp10 = models.CharField(max_length=2)
  countyfp10 = models.CharField(max_length=3)
  tractce10 = models.CharField(max_length=6)
  blockce10 = models.CharField(max_length=4)
  suffix1ce = models.CharField(max_length=1)
  geoid = models.CharField(max_length=16)
  name = models.CharField(max_length=11)
  mtfcc = models.CharField(max_length=5)
  ur10 = models.CharField(max_length=1)
  uace10 = models.CharField(max_length=5)
  funcstat = models.CharField(max_length=1)
  aland = models.FloatField()
  awater = models.FloatField()
  intptlat = models.CharField(max_length=11)
  intptlon = models.CharField(max_length=12)
  geom = models.MultiPolygonField(srid=4326)
  objects = models.GeoManager()

  def __unicode__(self):
    return self.name

def get_media_upload_dir(instance, filename):
    user_id  = instance.user.id
    upload_dir = "%s/%d/%s" % (settings.MEDIA_ROOT, user_id, filename)
    print "Upload dir set to: %s" % upload_dir
    return upload_dir

class Address_List(models.Model):
  user = models.ForeignKey(User)
  address_list = models.FileField(upload_to=get_media_upload_dir) 
