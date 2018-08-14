# Abandon all hope, ye who enter here.

from bs4 import BeautifulSoup
import datetime
import json
import requests
import dining_utils
import urllib.parse

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
    def parse_grams(s):
        if s == '': #sometimes it's just a plain empty string?
            return 0.0
        return float(s[:-1])
    def parse_milligrams(s):
        if s == '':
            return 0.0
        return float(s[:-2])
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
                if attribute_name == 'calories' or attribute_name == 'calories-from-fat':
                    if data == '':
                        continue
                    data = int(data)
                elif attribute_name == 'clean-diet-str':
                    diets = data.split(', ')
                    ret[item_name]['diets'] = diets
                    continue
                elif attribute_name in ['allergens', 'ingredient-list']:
                    data = dining_utils.parse_list(data)
                elif attribute_name in ['cholesterol', 'sodium']:
                    data = parse_milligrams(data)
                    attribute_name += '-mg'
                elif attribute_name in ['dietary-fiber', 'protein', 'sat-fat', 'sugars', 'total-carb', 'total-fat', 'trans-fat']:
                    data = parse_grams(data)
                    attribute_name += '-g'
                ret[item_name][attribute_name] = data
    return ret

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
    ret = {}
    for meal in r.keys():
        ret[meal] = {}
        for menu in r[meal].keys():
            ret[meal][menu] = _menu_html_to_dict(r[meal][menu])
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
