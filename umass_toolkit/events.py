import requests
from bs4 import BeautifulSoup

def _find_week_url():
	r = requests.get('https://umass.edu/events/')
	mysoup = BeautifulSoup(r.content, 'html.parser')
	url = mysoup.find("li", class_="body-nav-week").find("a").get("href")
	#href is to subdomain url
	return 'https://umass.edu{}'.format(url)

def _find_month_url():
	r = requests.get('https://umass.edu/events/')
	mysoup = BeautifulSoup(r.content, 'html.parser')
	url = mysoup.find("li", class_="body-nav-month").find("a").get("href")
	#href is to subdomain url
	return 'https://umass.edu{}'.format(url)
    
def _events(url):
	r = requests.get(url)
	mysoup = BeautifulSoup(r.content, 'html.parser')

    #container for list of today's events
	event_container = mysoup.find("div", class_="view-content")
	small_soup = BeautifulSoup(str(event_container), 'html.parser')
	event_list = small_soup.find_all("div", class_="event-details")

    #iterates through the event rows
	event_info = list()
	for unit in event_list:
		temp_soup = BeautifulSoup(str(unit), 'html.parser')
		temp_dict = {}
		temp_dict["name"] = temp_soup.find("span", class_="field-content").find("a").get_text().strip()
		temp_dict["description"] = temp_soup.find("div", class_="views-field-field-short-desc").find("div", class_="field-content").get_text().strip()
		temp_dict["date_time"] = temp_soup.find("h3", class_="event-date").get_text().strip()
		temp_dict["location"] = temp_soup.find("div", class_="event-location").get_text().strip()
		event_info.append(temp_dict)
	return event_info

def events_today():
	url = 'https://umass.edu/events/'
	return _events(url)

def events_this_week():
	url = _find_week_url()
	return _events(url)

def events_this_month():
	url = _find_month_url()
	return _events(url)
