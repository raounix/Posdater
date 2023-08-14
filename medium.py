import json
from bs4 import BeautifulSoup
import hashlib
import requests

def update_medium():
    print("Loading URLs. Please Wait")
    
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