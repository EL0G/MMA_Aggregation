import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

BASE_URL = "https://v1.mma.api-sports.io"

fighters_url = f"{BASE_URL}/fighters"
categories_url = f"{BASE_URL}/categories"

headers = {
    "x-apisports-key": os.getenv("API_KEY"),
}

weight_classes = requests.get(categories_url, headers=headers)
weight_classes_list = json.load(weight_classes.json()["response"])

all_fighters = []
for weight_class in weight_classes_list:
    params = {"category": weight_class}
    fighters = requests.get(fighters_url, headers=headers, params=params)
    all_fighters.extend(fighters.json()["response"])

with open("fighters.json", "w", encoding="utf-8") as file:
    json.dump(all_fighters, file, indent=4, ensure_ascii=False)
