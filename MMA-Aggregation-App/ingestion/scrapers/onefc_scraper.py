from bs4 import BeautifulSoup
import requests, http, json
import pandas as pd

BASE_URL = "https://www.onefc.com"


def onefc_events_scraper(url):
    all_events = []
    page_num = 1

    while True:
        if page_num == 1:
            url = f"{BASE_URL}/events/"
        else:
            url = f"{BASE_URL}/events/page/{page_num}/"

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
            all_events.append(
                {"title": title_element, "date": unix_date, "org": "OneFC"}
            )

        page_num += 1
    return all_events


def onefc_fighters_scraper():
    page_num = 1
    all_fighters = []

    while True:
        if page_num == 1:
            url = f"{BASE_URL}/athletes/"
        else:
            url = f"{BASE_URL}/athletes/page/{page_num}/"

        onefc_res = requests.get(url)
        if onefc_res.status_code == 404:
            print("Reached the end of the available event history.")
            break

        soup = BeautifulSoup(onefc_res.text, "lxml")
        fighters_info = soup.select(".simple-post-card.is-athlete")

        for fighter in fighters_info:
            fighter_text_info = fighter.select_one(".content")
            fighter_img_info = fighter.select_one(".image")

            if fighter_text_info:
                name = fighter.h3.text.strip()
                print(name)
                country = fighter.find(class_="country").text.strip()
                fighter_url = fighter.find("a")["href"]

                mma_fighter_page = requests.get(fighter_url)
                fighter_page_soup = BeautifulSoup(mma_fighter_page.text, "lxml")
                height_title = fighter_page_soup.find(
                    "h5", class_="title", string="Height"
                )
                height = height_title.find_next_sibling(
                    "div", class_="value"
                ).text.strip()

                attributes = fighter_page_soup.select(".attr")
                """for attribute in attributes:
                    attribute_title = attribute.select_one('.title')
                    print(attribute_title)
                    attribute_value = attribute.select_one('.value')
                    print(attribute_value)"""

            if fighter_img_info:
                fighter_img_link = fighter.find("img")["src"]

            # get age, height, weight, standardize, and put into table

            fighter_res = {
                "name": name,
                "country": country,
                "height": None,
                "weight_limit": None,
                "img": fighter_img_link,
                "Age": None,
                "url": fighter_url,
                "org": "OneFC",
            }
            all_fighters.append(fighter_res)

        page_num += 1

        print(f"page number: {page_num}")

    with open("return.json", "w") as file:
        json.dump(all_fighters, file, indent=4)


if __name__ == "__main__":
    onefc_fighters_scraper()
