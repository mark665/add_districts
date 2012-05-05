from django.contrib.gis.db import models

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

