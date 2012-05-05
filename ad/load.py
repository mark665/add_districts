import os
from django.contrib.gis.utils import LayerMapping
from models import Congress_Districts

congress_districts_mapping = {
    'statefp' : 'STATEFP',
    'cd112fp' : 'CD112FP',
    'geoid' : 'GEOID',
    'namelsad' : 'NAMELSAD',
    'lsad' : 'LSAD',
    'cdsessn' : 'CDSESSN',
    'mtfcc' : 'MTFCC',
    'funcstat' : 'FUNCSTAT',
    'aland' : 'ALAND',
    'awater' : 'AWATER',
    'intptlat' : 'INTPTLAT',
    'intptlon' : 'INTPTLON',
    'geom' : 'MULTIPOLYGON',
}

congress_districts = os.path.abspath('../shapes/tl_2011_us_cd112/tl_2011_us_cd112.shp')

def run(verbose=True):
  lm = LayerMapping(Congress_Districts, congress_districts, congress_districts_mapping, transform=True, source_srs='4269')

  lm.save(strict=True, verbose=verbose)



