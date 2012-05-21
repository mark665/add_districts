# Geocodes Document class file
import requests
import csv, sys
import simplejson

mapquest_osm_url = 'http://open.mapquestapi.com/nominatim/v1/search'
mapquest_url = 'http://www.mapquestapi.com/geocoding/v1/address'


def handle_uploaded_file(uploaded_file, districts_requested):

    # Create id variable for each row processed
    row_id = 1

    results = []

    addresses = uploaded_file.read().split('\n')

    
    for address in addresses:
        line = []

        line.append(row_id)
        row_id += 1
 
        line.append(address)

        payload = {
          'format': 'json',
          'q': address,
          'addressdetails': '1',
          'limit' : '1',
        }

        r = requests.get(mapquest_osm_url, params=payload)
        c = r.content
        j = simplejson.loads(c)

        line.append(j)

        results.append(line)


               



    return results
