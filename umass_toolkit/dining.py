# Abandon all hope, ye who enter here.

import datetime
import json
import requests
import urllib.parse
from . import dining_utils


def get_locations():
    locations = requests.get('https://www.umassdining.com/uapp/get_infov2').json()
    ret = []
    for location in locations:
        if location['opening_hours'] == 'Closed' or location['closing_hours'] == 'Closed':
            opening_hours = None
            closing_hours = None
        else:
            # TODO: this is horrific replace it
            opening_hours = datetime.datetime(2000, 1, 1).strptime(location['opening_hours'], '%I:%M %p').time()
            closing_hours = datetime.datetime(2000, 1, 1).strptime(location['closing_hours'], '%I:%M %p').time()
        ret.append({
            'name': location['location_title'],
            'id': location['location_id'],
            'opening_hours': opening_hours,
            'closing_hours': closing_hours,
        })
    return ret

def location_id_to_name(location_id):
    locations = get_locations()
    for location in locations:
        if location['id'] == location_id:
            return location['name']
    raise KeyError('no locations found with ID %d' % location_id)

def get_menu(location, date = datetime.date.today()):
    # If there is no menu available (for example, if the location is closed), then UMass Dining will simply return a blank page.
    # Status code is 200 no matter what...
    try:
        query_params = {'tid': location,
                        'date': date.strftime('%m/%d/%Y')}
        request_url = 'https://umassdining.com/foodpro-menu-ajax?' + urllib.parse.urlencode(query_params)
        r = requests.get(request_url).json()
    except json.decoder.JSONDecodeError:
        return []
    ret = []
    for meal in r.keys():
        for category in r[meal].keys():
            ret.extend(dining_utils.category_html_to_dict(r[meal][category], meal, category))
    return ret

def get_food_trucks():
    trucks = requests.get('https://www.umassdining.com/umassapi/truck_location').json()
    for key in trucks.keys():
        trucks[key]['id'] = int(key)
    trucks = [trucks[key] for key in trucks.keys()]

    def truck_is_open(truck):
        return truck['long'] != '' and truck['lat'] != ''

    ret = []
    for truck in trucks:
        truck_data = {
            'id': truck['id']
        }
        if truck_is_open(truck):
            truck_data['longitude'] = float(truck['long'])
            truck_data['latitude'] = float(truck['lat'])
            truck_data['is_open'] = True
        else:
            truck_data['is_open'] = False
        ret.append(truck_data)
    return ret
