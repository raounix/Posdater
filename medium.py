import json
from bs4 import BeautifulSoup
import hashlib
import requests

def update_articles(json_key,url):
    counter = 1
    data_file = open('./db/medium.json',"r+")
    accounts_json = json.load(data_file)
    accounts = accounts_json[json_key]
    for userid in accounts:
        last_posts = accounts[userid]
        medium_feed_url = url.format(userid)
        latest_posts = requests.get(medium_feed_url)
        all_posts = BeautifulSoup(latest_posts.text, "xml")
        all_items = all_posts.find_all('item')
        for item in all_items:
            hashed = hashlib.md5(item.title.text.encode()).hexdigest()
            if hashed not in last_posts:
                accounts_json[json_key][userid].append(hashed)
                print("{counter} - New Found ! - {title} : {url}\n".format(counter=str(counter),title=item.title.text,url=item.link.text))
                counter+=1
    data_file.close()
    with open("./db/medium.json", "w") as outfile:
        json.dump(accounts_json, outfile,indent=4)
    print("----------------------------------------------------------------\n")
    print("Done!")

def update_medium(type):
    print("Loading URLs. Please Wait")
    print("----------------------------------------------------------------\n")
    if (type == "account"):
        update_articles("accounts","https://medium.com/feed/{}")
    elif (type == "topic"):
        update_articles("topics","https://medium.com/feed/tag/{}")

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