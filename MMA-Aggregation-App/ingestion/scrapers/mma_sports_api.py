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

def get_all_fighters():
    """Gets MMA fighters from API by going through all weight classes"""
    all_fighters = []
    for weight_class in weight_classes_list:
        params = {"category": weight_class}
        fighters = requests.get(fighters_url, headers=headers, params=params)
        all_fighters.extend(fighters.json()["response"])
    return all_fighters

