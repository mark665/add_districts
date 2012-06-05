from django.contrib.gis.geos import Point
import requests
import csv
from ad.models import *
import json

mapquest_key = r'Fmjtd%7Cluua2duan1%2Cb2%3Do5-hrtx9'
mapquest_url = r'http://www.mapquestapi.com/geocoding/v1/batch?key=' + mapquest_key
mapquest_url_osm = r'http://open.mapquestapi.com/nominatim/v1/search?'

options_list = {'States':('state',States),
                'Counties':('county',Counties),
                'Congress_Districts':('cong',Congress_Districts),
#                'State_Leg_Upper':('stateuppr',State_Leg_Upper),
#                'State_Leg_Lower':('statelower',State_Leg_Lower),
#                'VTDs':('vtd',VTDs),
                'Blocks':('block',Blocks)}

def handle_uploaded_file(uploaded_address_list, districts_requested):

    results = add_districts(geocode_mapquest_batch(read_users_uploaded_csv(uploaded_address_list.address_list)), districts_requested)
    #results = add_districts(geocode_mapquest_osm(read_users_uploaded_csv(uploaded_file)), districts_requested)
    upload_file = open(str(uploaded_address_list.address_list), 'wb')
    write_results_to_file(upload_file,results)

    # once written, mark file as processed
    uploaded_address_list.processed=True
    uploaded_address_list.save()

    return results_to_geojson_dict(results)

def write_results_to_file(output_file,results):

    writer = csv.DictWriter(output_file, sorted(results[0].keys()))
    writer.writeheader()

    for row in results:
        writer.writerow(row)

    output_file.close()


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


def geocode_mapquest_batch(list_of_address_dictionaries):
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

def geocode_mapquest_osm(list_of_address_dictionaries):
    '''accepts lists of dictionaries, breaks up into chuncks of 100 per request
    dictionararies must contain keys: Address, City, State, Zip'''

    # return value will be a list of dictionaries (rows of labeled cells)
    results = list_of_address_dictionaries[:]

    for row in results:

        address_to_query = [row['Address'] + ' ' + row['City'] + ' ' + row['State'] + ' ' + row['Zip']]

        payload = {
          'format': 'json',
          'q': address_to_query,
          'addressdetails': '1',
          'limit' : '1',
        }
        
        geocode_response = requests.get(mapquest_url_osm, params=payload)

        if not list(geocode_response.json):
            row.update({'lat': ''})
            row.update({'long': ''})

        else:
            row.update({'lat': str(geocode_response.json[0]['lat'])})
            row.update({'long': str(geocode_response.json[0]['lon'])})

    return results
    

def add_districts(list_of_address_dictionaries_with_lat_lon, districts_requested):

    #list of dictionaries with lat lon key value pairs with districts
    results = []

    for line in list_of_address_dictionaries_with_lat_lon:

        # When lat or long are empty string, write all district values as empty strings
        if line['lat'] == '' or line['long'] == '':

            for district in districts_requested:
                try:
                    option_key, option_model = options_list[district]
                    line.update({option_key:''})
                except KeyError:
                    print "That district isn't configured."

            results.append(line)
            print line

        # do all the district lookups
        else:
            address_point = Point(float(line['long']), float(line['lat']))
 
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
            print line

    return results


def results_to_geojson_dict(results):

    #Convert the results list from above function to a geojson feature collection

    geojson_features  =[]

    for line in results:

        # When lat or long are empty string, write all district values as empty strings
        if line['lat'] == '' or line['long'] == '':
             pass

        else:
            geojson_features.append(line_to_geojson_feature(line))

    geojson_dict = {
        "type": "FeatureCollection",
         "features": geojson_features,
    }
    
    return geojson_dict


def line_to_geojson_feature(line):

    popup_content = ''

    #build the content of the popup
    for item in line:
        if item not in ('ad_id','lat','long','State','Zip4','VANID'): 
            popup_content += str(item).title() + ': ' + str(line[item]) +  '<br>'

        
    #Convert the line dict from above into a geojson feature
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [str(line['long']), str(line['lat'])]
        },
        "properties": {
            "address": line['Address'],
            "popupContent": popup_content 
        },
        "id": line['ad_id'],
    }
