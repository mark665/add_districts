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

class CD(models.Model):

  version = models.ForeignKey(Version)
  




  def __unicode__(self):
  	return str(self)

