from bs4 import BeautifulSoup
import requests, http, json
import pandas as pd


def onefc_scraper(url):
    all_events = []
    page_num = 1

    while True:
        if page_num == 1:
            url = "https://www.onefc.com/events/"
        else:
            url = f"https://www.onefc.com/events/page/{page_num}/"

        onefc_res = requests.get(url)
        if onefc_res.status_code == 404:
            print("Reached the end of the available event history.")
            break

        soup = BeautifulSoup(onefc_res.text, "lxml")
        events = soup.find_all(class_="simple-post-card")

        # If no matching cards are discovered on a page, break out safely
        if not events:
            print("No event cards uncovered on this page layer.")
            break

        # Extract titles and dates out of the currently loaded page layout
        for event in events:
            title_element = event.find(class_="title").text.strip()
            date_element = event.find(class_="datetime")
            unix_date = date_element["data-timestamp"]
            all_events.append({"title": title_element, "date": unix_date})

        page_num += 1
    return all_events
