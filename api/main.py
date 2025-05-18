from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import hashlib
import json
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DATA_FILE = "./medium.json"

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"accounts": [], "topics": []}, f, indent=4)


class AddItem(BaseModel):
    value: str


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def fetch_medium_posts(feed_url, category_type):
    try:
        res = requests.get(feed_url, timeout=10)
        soup = BeautifulSoup(res.content, "xml")
        items = soup.find_all("item")
        return [
            {
                "title": item.title.text,
                "url": item.link.text,
                "category": category_type,
            }
            for item in items
        ]
    except Exception:
        return []


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    data = load_data()
    all_posts = []

    for account in data["accounts"]:
        feed_url = f"https://medium.com/feed/{account}"
        all_posts.extend(fetch_medium_posts(feed_url, account))

    for topic in data["topics"]:
        feed_url = f"https://medium.com/feed/tag/{topic}"
        all_posts.extend(fetch_medium_posts(feed_url, topic))

    return templates.TemplateResponse("posts.html", {
        "request": request,
        "posts": all_posts,
        "topics": data["topics"],
        "accounts": data["accounts"]
    })


@app.post("/add-topic")
def add_topic(item: AddItem):
    data = load_data()
    if item.value in data["topics"]:
        raise HTTPException(status_code=400, detail="Topic already exists.")
    data["topics"].append(item.value)
    save_data(data)
    return {"message": "Topic added successfully."}


@app.post("/add-account")
def add_account(item: AddItem):
    data = load_data()
    if item.value in data["accounts"]:
        raise HTTPException(status_code=400, detail="Account already exists.")
    data["accounts"].append(item.value)
    save_data(data)
    return {"message": "Account added successfully."}


@app.delete("/remove-topic")
def remove_topic(item: AddItem):
    data = load_data()
    if item.value not in data["topics"]:
        raise HTTPException(status_code=404, detail="Topic not found.")
    data["topics"].remove(item.value)
    save_data(data)
    return {"message": "Topic removed successfully."}


@app.delete("/remove-account")
def remove_account(item: AddItem):
    data = load_data()
    if item.value not in data["accounts"]:
        raise HTTPException(status_code=404, detail="Account not found.")
    data["accounts"].remove(item.value)
    save_data(data)
    return {"message": "Account removed successfully."}
