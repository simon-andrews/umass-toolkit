import deans_list
import requests
from bs4 import BeautifulSoup

#query = {"title" : "cason", "field-major-value" : ""}
#r = requests.get("http://www.umass.edu/registrar/students/deans-list", params=query)
#mysoup = BeautifulSoup(r.content, 'html.parser')
#table of students is isolated from rest of html doc
#student_table = mysoup.find("table", class_="views-table cols-4")

#print(student_table)
#print(student_table.type)

#student_table = str(student_table)

print(deans_list.search_all_pages(name="cason"))