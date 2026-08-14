from bs4 import BeautifulSoup
import requests, http, json


def pfl_scraper(site_req):
    events_list = []
    site_html = BeautifulSoup(site_req.text, "lxml")
    events = site_html.find_all(class_="event-card-info p-4")

    for event in events:
        title = event.find("h3").text.strip()
        date = event.find("h6").text.strip()
        events_list.append(
            {
                "date": date,
                "title": title,
            }
        )
    return events_list

