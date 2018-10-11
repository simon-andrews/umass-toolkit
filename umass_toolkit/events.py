import requests
from bs4 import BeautifulSoup

#All of this code about dates and months is to get the week of the year for the url in events_this_week
class dated:
	def __init__(self, year, month, day):
		self.year = year
		self.month = month
		self.day = day

def week_of_year(x):
	if x.year%4 == 0:
		return (sum_months(x.month) + x.day + 1)%7
	else:
		return (sum_months(x.month) + x.day)%7

def sum_months(month):
	lst = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	total = 0
	for i in range(month-1):
		total += lst[i]
	return total

def events_today():
	r = requests.get("http://www.umass.edu/events")
	mysoup = BeautifulSoup(r.content, 'html.parser')

    #container for list of today's events
	event_container = mysoup.find("div", class_="view-events")
	small_soup = BeautifulSoup(str(event_container), 'html.parser')
	event_list = small_soup.find_all("div", class_="views-row")

    #iterates through the event rows
	event_info = list()
	for unit in event_list:
		temp_soup = BeautifulSoup(str(unit), 'html.parser')
		temp_dict = {}
		temp_dict["name"] = temp_soup.find("span", class_="field-content").find("a").get_text().strip()
		temp_dict["description"] = temp_soup.find("div", class_="views-field-field-short-desc").find("div", class_="field-content").get_text().strip()
		temp_dict["date_time"] = temp_soup.find("h3", class_="event-date").get_text().strip()
		temp_dict["location"] = temp_soup.find("div", class_="event-location").find("h3").get_text().strip()
		event_info.append(temp_dict)
	return event_info

