import requests
from bs4 import BeautifulSoup

def search(name="", major="", page=0):
    query = {"title" : name, "field-major-value" : major, "page": page}
    r = requests.get("http://www.umass.edu/registrar/students/deans-list", params=query)
    mysoup = BeautifulSoup(r.content, 'html.parser')

    #table of students is isolated from rest of html doc
    student_table = mysoup.find("table", class_="views-table cols-4")

    smaller_soup = BeautifulSoup(str(student_table), 'html.parser')
    student_list = smaller_soup.find_all("tr")

    #first tr tag has the table header, which isn't useful
    if len(student_list) == 0:
        return list()
    student_list.pop(0)

    #iterating through tr tags, each of which represents an individual in the search results, and adding them to a list
    student_info = list()
    for unit in student_list:
        temp_soup = BeautifulSoup(str(unit), 'html.parser')
        temp_dict = {}
        temp_dict["honors"] = "(H)" in str(temp_soup.find("td", class_="views-field views-field-field-honors").get_text())
        temp_dict["name"] = str(temp_soup.find("td", class_="views-field views-field-title").get_text()).strip()
        temp_dict["graduation_year"] = str(temp_soup.find("td", class_="views-field views-field-field-grad-year").get_text()).strip()
        temp_dict["major"] = str(temp_soup.find("td", class_="views-field views-field-field-major").get_text()).strip()
        student_info.append(temp_dict)
    return student_info

#extnding the search function so that it gets all of the search results, not just those on a specific page
def search_all_pages(name="", major=""):
    counter = 0
    current = search(name = name, major = major, page = counter)
    total = list()
    total += current
    while not len(current) == 0:
        counter += 1
        current = search(name = name, major = major, page = counter)
        total += current
    return total
