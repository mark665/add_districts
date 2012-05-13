import os
from django.contrib.gis.utils import LayerMapping
from models import Congress_Districts, Counties, States, Blocks

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

counties_mapping = {
    'statefp10' : 'STATEFP10',
    'countyfp10' : 'COUNTYFP10',
    'countyns10' : 'COUNTYNS10',
    'geoid10' : 'GEOID10',
    'name10' : 'NAME10',
    'namelsad10' : 'NAMELSAD10',
    'lsad10' : 'LSAD10',
    'classfp10' : 'CLASSFP10',
    'mtfcc10' : 'MTFCC10',
    'csafp10' : 'CSAFP10',
    'cbsafp10' : 'CBSAFP10',
    'metdivfp10' : 'METDIVFP10',
    'funcstat10' : 'FUNCSTAT10',
    'aland10' : 'ALAND10',
    'awater10' : 'AWATER10',
    'intptlat10' : 'INTPTLAT10',
    'intptlon10' : 'INTPTLON10',
    'geom' : 'MULTIPOLYGON',
}

state_mapping = {
    'region' : 'REGION',
    'division' : 'DIVISION',
    'statefp' : 'STATEFP',
    'statens' : 'STATENS',
    'geoid' : 'GEOID',
    'stusps' : 'STUSPS',
    'name' : 'NAME',
    'lsad' : 'LSAD',
    'mtfcc' : 'MTFCC',
    'funcstat' : 'FUNCSTAT',
    'aland' : 'ALAND',
    'awater' : 'AWATER',
    'intptlat' : 'INTPTLAT',
    'intptlon' : 'INTPTLON',
    'geom' : 'MULTIPOLYGON',
}

blocks_mapping = {
    'statefp' : 'STATEFP',
    'countyfp' : 'COUNTYFP',
    'statefp10' : 'STATEFP10',
    'countyfp10' : 'COUNTYFP10',
    'tractce10' : 'TRACTCE10',
    'blockce10' : 'BLOCKCE10',
    'suffix1ce' : 'SUFFIX1CE',
    'geoid' : 'GEOID',
    'name' : 'NAME',
    'mtfcc' : 'MTFCC',
    'ur10' : 'UR10',
    'uace10' : 'UACE10',
    'funcstat' : 'FUNCSTAT',
    'aland' : 'ALAND',
    'awater' : 'AWATER',
    'intptlat' : 'INTPTLAT',
    'intptlon' : 'INTPTLON',
    'geom' : 'MULTIPOLYGON',
}


congress_districts = os.path.abspath('../shapes/tl_2011_us_cd112/tl_2011_us_cd112.shp')

counties = os.path.abspath('../shapes/TIGER2010/COUNTY/tl_2010_us_county10/tl_2010_us_county10.shp')

states = os.path.abspath('../shapes/TIGER2011/STATE/tl_2011_us_state.shp')

blocks = os.path.abspath('../shapes/TABBLOCK/tl_2011_53_tabblock.shp')



def run(verbose=True):
  lm = LayerMapping(Blocks, blocks, blocks_mapping, transform=True, source_srs='4269', encoding='iso-8859-1')

  lm.save(strict=True, verbose=verbose)



