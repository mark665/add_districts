from django.contrib.gis.geos import Point
import requests
from ad.models import *

mapquest_osm_url = 'http://open.mapquestapi.com/nominatim/v1/search'
mapquest_url = 'http://www.mapquestapi.com/geocoding/v1/address'


def handle_uploaded_file(uploaded_file, districts_requested):

    # Create id variable for each row processed
    row_id = 1

    # return value will be a list of lists (rows of cells)
    results = []

    #TODO read file as a csv with error checking, until then:
    # unpack address file on newlines
    addresses = uploaded_file.read().split('\n')
    # get rid of cruft
    addresses.pop(-1)
    
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

            #TODO handle lookups that aren't found.

            if district == 'States':
                line.append(States.objects.get(geom__contains = address_point).name) 

            if district == 'Counties':
                line.append(Counties.objects.get(geom__contains = address_point).name10)

            if district == 'Congress_Districts':
                line.append(Congress_Districts.objects.get(geom__contains = address_point).cd112fp)    
 
            if district == 'State_Leg_Upper':
                line.append(State_Leg_Upper.objects.get(geom__contains = address_point)) 

            if district == 'State_Leg_Lower':
                line.append(State_Leg_Lower.objects.get(geom__contains = address_point))

            if district == 'Precinct':
                line.append(VTDs.objects.get(geom__contains = address_point))

            if district == 'Blocks':
                line.append(Blocks.objects.get(geom__contains = address_point).name)  

        results.append(line)


    return results
