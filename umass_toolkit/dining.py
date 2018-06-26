from bs4 import BeautifulSoup
from pprint import pprint
import datetime
import requests

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

def _menu_html_to_dict(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    items = soup.find_all('a', href='#inline')
    ret = {}
    for item in items:
        item_name = item.string
        ret[item_name] = {}
        for attribute in item.attrs.keys():
            if attribute.startswith('data-'):
                if attribute.endswith('dv') or attribute in ['data-dish-name', 'data-recipe-webcode']:
                    continue
                attribute_name = attribute[5:]
                data = item.attrs[attribute]
                if attribute_name == 'allergens':
                    data = [x.strip() for x in data.split(', ')]
                elif attribute_name == 'calories' or attribute_name == 'calories-from-fat':
                    data = int(data)
                elif attribute_name == 'clean-diet-str':
                    diets = item.attrs[attribute].join('').split(', ')
                    ret[item_name]['diets'] = diets
                    continue
                # TODO: parse the ingredient list
                ret[item_name][attribute[5:]] = data
    return ret

def get_menu(location):
    r = requests.get('https://umassdining.com/foodpro-menu-ajax?tid=' + str(location)).json()
    ret = {}
    for meal in r.keys():
        ret[meal] = {}
        for menu in r[meal].keys():
            ret[meal][menu] = _menu_html_to_dict(r[meal][menu])
    return ret

def get_food_trucks():
    trucks = requests.get('https://www.umassdining.com/umassapi/truck_location').json()
    ret = []
    for truck_id in trucks.keys():
        int_id = int(truck_id)
        ret.append({
            'id': int_id,
            'longitude': float(trucks[truck_id]['long']) if trucks[truck_id]['long'] != '' else None,
            'latitude': float(trucks[truck_id]['lat']) if trucks[truck_id]['lat'] != '' else None,
        })
    return ret
