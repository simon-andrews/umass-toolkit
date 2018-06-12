import requests
import time


class Person:
    def __init__(self, data):
        self.name = None
        self.email = None
        self.affiliations = []
        self.majors = []
        self.title = None
        self.phone_numbers = []
        self.buildings = []
        self.departments = []
        self.urls = []
        for key in data.keys():
            if key == 'Name':
                self.name = data['Name']
            elif key == 'Email':
                self.email = data['Email']
            elif key == 'Affil':
                for affiliation in data['Affil']:
                    self.affiliations.append(affiliation)
            elif key == 'Major':
                for major in data['Major']:
                    self.majors.append(major)
            elif key == 'Title':
                self.title = data['Title']
            elif key == 'Phone':
                for phone_number in data['Phone']:
                    self.phone_numbers.append(phone_number)
            elif key == 'Building':
                for building in self.buildings:
                    self.buildings.append(building)
            elif key == 'Dept':
                for department in data['Dept']:
                    self.departments.append(department)
            elif key == 'URL':
                for url in data['URL']:
                    self.urls.append(url)

    def __str__(self):
        return '{} <{}>'.format(self.name, self.email)


def search(query):
    payload = {
        'q': query,
        'time': int(time.time() * 1000)
    }
    r = requests.post('https://www.umass.edu/peoplefinder/engine/', data=payload).json()
    overflowed = r['OverflowFlag']
    people = []
    for person in r['Results']:
        people.append(Person(person))
    return {'results': people, 'overflow_flag': overflowed}