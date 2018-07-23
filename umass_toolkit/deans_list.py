import requests
from bs4 import BeautifulSoup

def search(last_name):
    query = {"title" : last_name, "field-major-value" : ""}
    r = requests.get("http://www.umass.edu/registrar/students/deans-list", params=query)
    mysoup = BeautifulSoup(r.content, 'html.parser')

    #table of students is isolated from rest of html doc
    student_table = mysoup.find("table", class_="views-table cols-4")
    smaller_soup = BeautifulSoup(str(student_table), 'html.parser')
    student_list = smaller_soup.find_all("tr")

    #first tr tag has the table header, which isn't useful
    student_list.pop(0)

    #iterating through tr tags, each of which represents an individual in the search results, and adding them to a list
    student_info = list()
    for unit in student_list:
        temp_soup = BeautifulSoup(str(unit), 'html.parser')
        temp_dict = {}
        if "(H)" not in str(temp_soup.find("td", class_="views-field views-field-field-honors").get_text()):
            temp_dict["honors"] = False
        else:
            temp_dict["honors"] = True
        temp_dict["name"] = str(temp_soup.find("td", class_="views-field views-field-title").get_text())
        temp_dict["graduation_year"] = str(temp_soup.find("td", class_="views-field views-field-field-grad-year").get_text())
        temp_dict["major"] = str(temp_soup.find("td", class_="views-field views-field-field-major").get_text())
        student_info.append(temp_dict)
    return student_info
