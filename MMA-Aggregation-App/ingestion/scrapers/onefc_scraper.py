from bs4 import BeautifulSoup
import requests, http, json
import pandas as pd
import re

BASE_URL = "https://www.onefc.com"


def scraping_helper(path):

    page_num = 1

    while True:
        if page_num == 1:
            url = f"{BASE_URL}/{path}/"
        else:
            url = f"{BASE_URL}/{path}/page/{page_num}/"

        response = requests.get(url)

        if response.status_code == 404:
            break

        soup = BeautifulSoup(response.text, "lxml")

        yield soup

        page_num += 1


def scrape_fighter_stat(desired_stat, fighter_page_soup, pattern_match):
    stat_title = fighter_page_soup.find("h5", class_="title", string=desired_stat)

    if not stat_title:
        return None

    stat_value = stat_title.find_next_sibling("div", class_="value").text.strip()

    if not stat_value:
        return None

    return re.search(pattern_match, stat_value).group(1).strip()


def onefc_events_scraper():
    all_events = []

    for soup in scraping_helper("events"):
        events = soup.find_all(class_="simple-post-card")
        # Extract titles and dates out of the currently loaded page layout
        for event in events:
            title_element = event.find(class_="title").text.strip()
            date_element = event.find(class_="datetime")
            unix_date = date_element["data-timestamp"]
            mma_organization = "OneFC"

            all_events.append(
                {"title": title_element, "date": unix_date, "org": mma_organization}
            )

    return all_events


def onefc_fighters_scraper():
    all_fighters = []

    height_pattern = re.compile(r"(\d+) CM")
    age_pattern = re.compile(r"(\d+) Y")
    weight_pattern = re.compile(r"(\d+\.?\d*\s*)KG")

    for soup in scraping_helper("athletes"):
        fighters_info = soup.select(".simple-post-card.is-athlete")

        for fighter in fighters_info:
            fighter_text_info = fighter.select_one(".content")
            fighter_img_info = fighter.select_one(".image")

            if fighter_text_info:
                name = fighter.h3.text.strip()
                country = fighter.find(class_="country").text.strip()
                fighter_url = fighter.find("a")["href"]

                mma_fighter_page = requests.get(fighter_url)
                fighter_page_soup = BeautifulSoup(mma_fighter_page.text, "lxml")

                height_value = scrape_fighter_stat(
                    "Height", fighter_page_soup, height_pattern
                )
                age_value = scrape_fighter_stat("Age", fighter_page_soup, age_pattern)
                weight_value = scrape_fighter_stat(
                    "Weight Limit", fighter_page_soup, weight_pattern
                )

            if fighter_img_info:
                fighter_img_link = fighter.find("img")["src"]

            fighter_res = {
                "name": name,
                "country": country,
                "height": height_value,
                "weight_limit": weight_value,
                "img": fighter_img_link,
                "Age": age_value,
                "url": fighter_url,
                "org": "OneFC",
            }

            all_fighters.append(fighter_res)

    return all_fighters
