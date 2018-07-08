import requests
import time


def _create_person_dict(data):
    person = {}
    key_translations = {
        # People Finder API key -> "clean" UMass Toolkit key
        # Some have been made plural because they actually represent lists.
        'Name':     'name',
        'Email':    'email',
        'Affil':    'affiliations',
        'Major':    'majors',
        'Title':    'title',
        'Phone':    'phone_numbers',
        'Building': 'buildings',
        'Dept':     'departments',
        'URL':      'websites',
    }
    for key in data.keys():
        if key in key_translations.keys():
            person[key_translations[key]] = data[key]
    return person

def search(query):
    payload = {
        'q': query,
        'time': int(time.time() * 1000)
    }
    r = requests.post('https://www.umass.edu/peoplefinder/engine/', data=payload).json()
    overflowed = r['OverflowFlag']
    people = []
    for person in r['Results']:
        people.append(_create_person_dict(person))
    return {'people': people, 'overflow_flag': overflowed}
