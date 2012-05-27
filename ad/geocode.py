from django.contrib.gis.geos import Point
import requests
import csv
from ad.models import *
import json

mapquest_osm_url = 'http://open.mapquestapi.com/nominatim/v1/search'
mapquest_url = 'http://www.mapquestapi.com/geocoding/v1/address'


def handle_uploaded_file(uploaded_file, districts_requested):

    # Create id variable for each row processed
    row_id = 1

    # return value will be a list of lists (rows of cells)
    results = []

    # TODO use csv.Sniffer to handle appropriate dialect
    # TODO Strip out commas from addresses (and other troublesome characters)
    
    # open file as csv unpack on newlines
    addresses = csv.reader(uploaded_file.read().split('\n')[:-1])
    
    for address in addresses:

        # hold this line as a list
        line = []

        # first element in list of line is
        # an id that increments for each loop over the row
        line.append(row_id)
        row_id += 1
 
        # second element in line list is address column row
        line.append(address)

        # pack same address into a requests payload
        payload = {
          'format': 'json',
          'q': address,
          'addressdetails': '1',
          'limit' : '1',
        }
        
        r = requests.get(mapquest_osm_url, params=payload)
        
        latitude, longitude = r.json[0]['lat'], r.json[0]['lon']

        line.append(latitude)
        line.append(longitude)

        address_point = Point(float(longitude), float(latitude))

        for district in districts_requested:

            if district == 'states':
                try:
                    line.append(States.objects.get(geom__contains = address_point).name)
                except States.DoesNotExist:
                    line.append('')

            if district == 'counties':
                try:
                    line.append(Counties.objects.get(geom__contains = address_point).name10)
                except Counties.DoesNotExist:
                    line.append('')

            if district == 'congress_districts':
                try:
                    line.append(Congress_Districts.objects.get(geom__contains = address_point).cd112fp)
                except Congress_Districts.DoesNotExist:
                    line.append('')

            if district == 'state_leg_upper':
                try:
                    line.append(State_Leg_Upper.objects.get(geom__contains = address_point))
                except State_Leg_Upper.DoesNotExist:
                    line.append('')

            if district == 'state_leg_lower':
                try:
                    line.append(State_Leg_Lower.objects.get(geom__contains = address_point))
                except State_Leg_Lower.DoesNotExist:
                    line.append('')

            if district == 'vtds':
                try:
                    line.append(VTDs.objects.get(geom__contains = address_point))
                except VTDs.DoesNotExist:
                    line.append('')

            if district == 'blocks':
                try:
                    line.append(Blocks.objects.get(geom__contains = address_point).name)
                except Blocks.DoesNotExist:
                    line.append('')

        results.append(line)


    return results
    
def list_to_geojson_dict(result_list):

    #Convert the results list from above function to a geojson dict
    #Some of this code can be eliminated if the result object in the above function is created
    # as a dict
    
    geojson_dict = {
        "type": "FeatureCollection",
        "features": [crime_to_geojson(crime) for crime in crimes]
    }
    
    return HttpResponse(json.dumps(geojson_dict), content_type='application/json')

def result_to_geojson_feature(result):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [result.pt.x, result.pt.y]
        },
        "properties": {
            "description": result.description
        },
        "id": result.id,
    }