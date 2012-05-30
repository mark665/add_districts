from django.contrib.gis.geos import Point
import requests
import csv
from ad.models import *
import json

mapquest_osm_url = 'http://open.mapquestapi.com/nominatim/v1/search'
mapquest_url = 'http://www.mapquestapi.com/geocoding/v1/address'

options_list = {'States':('state',States),'Counties':('county',Counties),
                'Congress_Districts':('cong',Congress_Districts),
#                'State_Leg_Upper':('stateuppr',State_Leg_Upper),
#                'State_Leg_Lower':('statelower',State_Leg_Lower),
#                'VTDs':('vtd',VTDs),
                'Blocks':('block',Blocks)}

def handle_uploaded_file(uploaded_file, districts_requested):

    # Create id variable for each row processed
    row_id = 1

    # return value will be a list of dicts (rows of cells)
    results = []

    # TODO use csv.Sniffer to handle appropriate dialect
    # TODO Strip out commas from addresses (and other troublesome characters)
    
    # open file as csv unpack on newlines
    addresses = csv.reader(uploaded_file.read().split('\n')[:-1])
    
    for address in addresses:

        # hold this line as a dict
        line = {}

        # first key:value pair in line is
        # an id that increments for each loop over the row
        line.update({'id':row_id})
        row_id += 1
 
        # second key:value pair in line is address
        line.update({'addr':address})

        # pack same address into a requests payload for the mapquest geocoding api
        payload = {
          'format': 'json',
          'q': address,
          'addressdetails': '1',
          'limit' : '1',
        }
        
        r = requests.get(mapquest_osm_url, params=payload)
        
        latitude, longitude = r.json[0]['lat'], r.json[0]['lon']
        
        # third and fourth key:value pairs
        line.update({'lat':latitude})
        line.update({'long':longitude})

        address_point = Point(float(longitude), float(latitude))
        
        print districts_requested
        #add additional key:value pairs 
        for district in districts_requested:
            try:
                option_key, option_model = options_list[district]
            except KeyError :
                continue
            try:
                line.update({option_key:str(option_model.objects.get(geom__contains = address_point))})
            except option_model.DoesNotExist:
                line.update({key:''})

        results.append(line)

    return results_to_geojson_dict(results)

def results_to_geojson_dict(results):

    #Convert the results list from above function to a geojson feature collection
    geojson_dict = {
        "type": "FeatureCollection",
        "features": [line_to_geojson_feature(i) for i in results]
    }
    
    return geojson_dict

def line_to_geojson_feature(line):

    #Convert the line dict from above into a geojson feature
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [str(line['long']), str(line['lat'])]
        },
        "properties": {
            "address": line['addr'],
            #TODO add in more dict items
            "popupContent": "%s" %(line['state']) 
        },
        "id": line['id'],
    }
