from django.contrib.gis.geos import Point
import requests
import csv
from ad.models import *
import json

mapquest_key = r'Fmjtd%7Cluua2duan1%2Cb2%3Do5-hrtx9'
mapquest_url = r'http://www.mapquestapi.com/geocoding/v1/batch?key=' + mapquest_key

options_list = {'States':('state',States),
                'Counties':('county',Counties),
                'Congress_Districts':('cong',Congress_Districts),
#                'State_Leg_Upper':('stateuppr',State_Leg_Upper),
#                'State_Leg_Lower':('statelower',State_Leg_Lower),
#                'VTDs':('vtd',VTDs),
                'Blocks':('block',Blocks)}

def handle_uploaded_file(uploaded_file, districts_requested):

    results = add_districts(batch_geocode(read_users_uploaded_csv(uploaded_file)), districts_requested)

    f = open('output.csv', 'wb')

    writer = csv.DictWriter(f, sorted(results[0].keys()))
    writer.writeheader()

    for row in results:
        writer.writerow(row)

    f.close()

    return results_to_geojson_dict(results)


def read_users_uploaded_csv(uploaded_file):
    '''opens user supplied csv file and creates list of dictionaries'''

    dialect = csv.Sniffer().sniff(uploaded_file.read(1024))
    uploaded_file.seek(0)
    addresses = csv.reader(uploaded_file, dialect)

    # return value will be a list of dictionaries (rows of labeled cells)
    results = []

    # save first row as headers list
    csv_headers = addresses.next()

    # Create id variable for each row processed
    ad_id = 1

    for address in addresses:

        # hold this line as a dict
        line = {}

        # add an id that increments for each loop over row
        line.update({'ad_id':ad_id})
        ad_id += 1

        # use header for dict keys, address row for values
        line.update(dict(zip((csv_headers), (address))))

        # add this row to result list
        results.append(line)

    return results


def batch_geocode(list_of_address_dictionaries):
    '''accepts lists of dictionaries, breaks up into chuncks of 100 per request
    dictionararies must contain keys: Address, City, State, Zip'''

    # return value will be a list of dictionaries (rows of labeled cells)
    results = []

    def batches_of(rows, n=100):
        '''yield successive n-sized chunks'''
        for row in xrange(0, len(rows), n):
            yield rows[row:row + n]

    for batch in batches_of(list_of_address_dictionaries):

        # make a copy for reassembly as results
        batch_results = batch[:]

        # package up addresses the way mapquest likes (in batch size)
        addresses_to_query = []

        for row in batch:

            #TODO add if ZIP 4 

            address_to_query= row['Address'] + ' ' + row['City'] + ' ' + row['State'] + ' ' + row['Zip']
            addresses_to_query.append(address_to_query)

        payload = {
          'location': addresses_to_query,
          'thumbMaps': 'false',
          'maxResults' : '1',
          'output': 'json'
        }

        geocode_response = requests.get(mapquest_url, params=payload)

        latitude_results = []
        longitude_results = []

        for line in geocode_response.json['results']:

            try:
                latitude_results.append({'lat': str(line['locations'][0]['displayLatLng']['lat'])} )
                longitude_results.append({'long': str(line['locations'][0]['displayLatLng']['lng'])} )

            except:
                latitude_results.append({'lat': ''})
                longitude_results.append({'long': ''})

        map(lambda x, y: x.update(y), batch_results, latitude_results)
        map(lambda x, y: x.update(y), batch_results, longitude_results)
        
        for value in batch_results:
            results.append(value)

    return results
        

def add_districts(list_of_address_dictionaries_with_lat_lon, districts_requested):

    #list of dictionaries with lat lon key value pairs with districts
    results = []

    for line in list_of_address_dictionaries_with_lat_lon:

        # handle empty strings converstion to float throws error.

        if not line['long'] == '':
            address_point = Point(float(line['long']), float(line['lat']))
        else:
            address_point = None

        #add additional key:value pairs 
        for district in districts_requested:
            try:
                option_key, option_model = options_list[district]
            except KeyError :
                continue
            try:
                line.update({option_key:str(option_model.objects.get(geom__contains = address_point))})
            except option_model.DoesNotExist:
                line.update({option_key:''})

        results.append(line)

    return results


def results_to_geojson_dict(results):

    #Convert the results list from above function to a geojson feature collection
    geojson_dict = {
        "type": "FeatureCollection",
        "features": [line_to_geojson_feature(i) for i in results]
    }
    
    return geojson_dict


def line_to_geojson_feature(line):

    popup_content = ''

    #build the content of the popup
    for item in line:
        if not (item == 'ad_id'): 
            popup_content += str(line[item]) +  '<br>'
        
    #Convert the line dict from above into a geojson feature
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [str(line['long']), str(line['lat'])]
        },
        "properties": {
            "address": line['Address'],
            #TODO add in more dict items
            "popupContent": popup_content 
        },
        "id": line['ad_id'],
    }
