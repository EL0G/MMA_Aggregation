from bs4 import BeautifulSoup
import requests, http, json


def rizin_scraper(site_req):
    events_list = []
    site_html = BeautifulSoup(site_req.text, "lxml")
    events = site_html.find_all(
        "div",
        class_="person",
    )

    for event in events:
        event_info = event.find("h4")
        info_parts = list(event_info.stripped_strings)

        date = info_parts[0].strip()
        event_name = " ".join(info_parts[1:]).strip()
        events_list.append(
            {
                "date": date,
                "title": event_name,
            }
        )
    return events_list
