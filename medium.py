import json
from bs4 import BeautifulSoup
import hashlib
import requests

def update_accounts():
    data_file = open('./db/medium.json',"r+")
    accounts_json = json.load(data_file)
    accounts = accounts_json['accounts']
    for userid in accounts:
        last_posts = accounts[userid]
        medium_feed_url = "https://medium.com/feed/{}".format(userid)
        latest_posts = requests.get(medium_feed_url)
        all_posts = BeautifulSoup(latest_posts.text, "xml")
        all_items = all_posts.find_all('item')
        for item in all_items:
            hashed = hashlib.md5(item.title.text.encode()).hexdigest()
            if hashed not in last_posts:
                accounts_json['accounts'][userid].append(hashed)
                print("New Found ! - {title} : {url}".format(title=item.title.text,url=item.link.text))

    data_file.close()
    with open("./db/medium.json", "w") as outfile:
        json.dump(accounts_json, outfile,indent=4)

    print("Done!")

def update_topics():
    data_file = open('./db/medium.json',"r+")
    accounts_json = json.load(data_file)
    accounts = accounts_json['topics']
    for userid in accounts:
        last_posts = accounts[userid]
        medium_feed_url = "https://medium.com/feed/tag/{}".format(userid)
        latest_posts = requests.get(medium_feed_url)
        all_posts = BeautifulSoup(latest_posts.text, "xml")
        all_items = all_posts.find_all('item')
        for item in all_items:
            hashed = hashlib.md5(item.title.text.encode()).hexdigest()
            if hashed not in last_posts:
                accounts_json['topics'][userid].append(hashed)
                print("New Found ! - {title} : {url}".format(title=item.title.text,url=item.link.text))

    data_file.close()
    with open("./db/medium.json", "w") as outfile:
        json.dump(accounts_json, outfile,indent=4)

    print("Done!")

def update_medium(type):
    print("Loading URLs. Please Wait")
    if (type == "account"):
        update_accounts()
    elif (type == "topic"):
        update_topics()

def add_medium_account(userID):
    data_file = open('./db/medium.json',"r+")
    accounts_json = json.load(data_file)
    if userID not in accounts_json['accounts']:
        accounts_json['accounts'][userID] = []
        with open("./db/medium.json", "w") as outfile:
            json.dump(accounts_json, outfile,indent=4)
        print("Account added successfully!")
    else:
        print("Account is Already in DB!")

def add_medium_topic(topic):
    data_file = open('./db/medium.json',"r+")
    topics_json = json.load(data_file)
    if topic not in topics_json['topics']:
        topics_json['topics'][topic] = []
        with open("./db/medium.json", "w") as outfile:
            json.dump(topics_json, outfile,indent=4)
        print("Topic added successfully!")
    else:
        print("Topic is Already in DB!")