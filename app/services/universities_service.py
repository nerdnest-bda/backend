from flask import current_app
from bson import Binary, ObjectId
from pymongo.errors import DuplicateKeyError
from pymongo import UpdateOne
from uuid import uuid4
import requests
from bs4 import BeautifulSoup
import re


def insert_batch(data):
    try:
        db = current_app.db
        universities_collection = db[current_app.config["COORDINATES_COLLECTION"]]

        bulk_operations = []

        for uni in data:
            # Calculate quadrant and set it explicitly
            lat = uni["coordinates"]["latitude"]
            lon = uni["coordinates"]["longitude"]
            quadrant = assign_us_quadrant(lat, lon)

            # Copy uni and remove 'quadrant' if present
            uni_insert = uni.copy()

            operation = UpdateOne(
                {"name": uni["name"], "coordinates": uni["coordinates"]},
                {
                    "$setOnInsert": uni_insert,
                    # "$set": {"quadrant": quadrant, "website": uni["website"]}
                },
                upsert=True
            )

            bulk_operations.append(operation)

        if bulk_operations:
            result = universities_collection.bulk_write(bulk_operations, ordered=False)
            return True, f"Inserted {result.upserted_count} new records, updated {result.modified_count} existing records."
        else:
            return True, "No data to process."

    except Exception as e:
        return False, str(e)

def assign_us_quadrant(lat, lon):
    us_center_lat = 39.8
    us_center_lon = -98.6
    if lat > us_center_lat and lon < us_center_lon:
        return "q1"  # Northwest (Top Left)
    elif lat > us_center_lat and lon > us_center_lon:
        return "q2"  # Northeast (Top Right)
    elif lat < us_center_lat and lon < us_center_lon:
        return "q3"  # Southwest (Bottom Left)
    else:
        return "q4"  # Southeast (Bottom Right)

def get_universities(data):
    try:
        db = current_app.db
        quadrant = assign_us_quadrant(data.latitude, data.longitude)
        print(quadrant)
        universities_collection = db[current_app.config["COORDINATES_COLLECTION"]]
        universities = list(universities_collection.find({"quadrant": quadrant}, {"_id": 1, "name": 1, "coordinates": 1, "quadrant": 1, "address": 1, "mascot_photo": 1, "website": 1}))
        return True, universities
    except Exception as e:
        return False, str(e)

def get_universities_via_id(id):
    try:
        db = current_app.db
        universities_collection = db[current_app.config["COORDINATES_COLLECTION"]]
        university = universities_collection.find_one({"_id": id})
        print("MY university", university)
        return True, university
    except Exception as e:
        return False, str(e)  
    
def get_about(college_name: str):
    try:
        url = f"https://en.wikipedia.org/w/api.php"
        params = {
            "action": "parse",
            "page": college_name,
            "format": "json",
            "prop": "text",
            "formatversion": 2,
            "redirects": 1
        }

        res = requests.get(url, params=params)
        data = res.json()
        
        if 'error' in data:
            return False, None
        
        html_content = data['parse']['text']
        soup = BeautifulSoup(html_content, 'html.parser')

        for sup in soup.find_all("sup"):
            sup.decompose()

        
        paragraphs = soup.find_all('p')
        text_parts = []
        for p in paragraphs:
            clean_text = p.get_text(separator=" ", strip=True)
            clean_text = re.sub(r'\s+', ' ', clean_text)
            if clean_text:
                text_parts.append(clean_text)
            if len(text_parts) >= 3:
                break
        return True, "\n\n".join(text_parts)
    
    except Exception as e:
        return False, str(e)
    

def get_logo(college_name: str):
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "parse",
            "page": college_name,
            "format": "json",
            "prop": "text",
            "formatversion": 2,
            "redirects": 1  # follow redirects to actual page
        }

        res = requests.get(url, params=params)
        data = res.json()

        if 'error' in data:
            return False, "Wikipedia page not found"

        html_content = data['parse']['text']
        soup = BeautifulSoup(html_content, 'html.parser')

        infobox = soup.find("table", class_="infobox")
        img_tag = infobox.find("img") if infobox else None

        if not img_tag:
            return False, "No logo found on Wikipedia page"

        logo_url = "https:" + img_tag["src"]
        return True, logo_url

    except Exception as e:
        return False, str(e)
