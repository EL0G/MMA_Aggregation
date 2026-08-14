import re
import requests
from bs4 import BeautifulSoup
import json


def ufc_scraper(site_req):
    events_list = []
    site_html = BeautifulSoup(site_req.text, "lxml")
    events_info = site_html.find_all(class_="UfcSchedule-info")

    for event in events_info:
        parts = list(event.stripped_strings)
        date = parts[0]
        title = parts[1]

        events_list.append(
            {
                "date": date,
                "title": title,
            }
        )

    return events_list

