import psycopg
import os
from dotenv import load_dotenv
import datetime
import requests
import pandas as pd
from scrapers.rizin_scraper import rizin_scraper
from scrapers.ufc_scraper import ufc_scraper
from scrapers.pfl_scraper import pfl_scraper
from scrapers.onefc_scraper import onefc_scraper
from processing.normalize import normalize_dates

load_dotenv()

db_host = os.getenv("HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")

conn = psycopg.connect(
    host=db_host, dbname=db_name, user=db_user, password=db_pass, port=db_port
)

cur = conn.cursor()

mma_sources = {
    "ufc": {
        "url": "https://www.cbssports.com/ufc/schedule/results/",
        "scraper": ufc_scraper,
    },
    "pfl": {
        "url": "https://pflmma.com/events",
        "scraper": pfl_scraper,
    },
    "rizin": {
        "url": "https://jp.rizinff.com/_tags/%E5%A4%A7%E4%BC%9A%E6%83%85%E5%A0%B1",
        "scraper": rizin_scraper,
    },
    "one_fc": {"url": "https://www.onefc.com/events/", "scraper": onefc_scraper},
}


query = """
        INSERT INTO MMA_events(event_name, event_date)
        VALUES (%s, %s)
        ON CONFLICT (event_name, event_date)
        DO NOTHING
        """


def load_data(data):
    for params in data:
        mma_data = (params["title"], params["date"])
        cur.execute(query, mma_data)

    conn.commit()


def ingestion_pipeline(source):
    # Extract
    url = mma_sources[source]["url"]
    url_req = requests.get(url)
    scrape_func = mma_sources[source]["scraper"]
    scraped_data = scrape_func(url_req)
    # Transform
    normalized_data = normalize_dates(scraped_data, source)

    # Load
    load_data(normalized_data)


for source in mma_sources:
    ingestion_pipeline(source)
