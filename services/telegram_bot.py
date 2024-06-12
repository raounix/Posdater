import telegram
import asyncio
import json
import sys
import time
from telegram.request import HTTPXRequest

sys.path.append("../")
import medium


def initialize():
    json_file = open('../env_files/telegram.json')
    data = json.load(json_file)
    return data


async def send(chat_id):
    for topic_link in topics:
        try:
            await bot.send_message(chat_id=chat_id, text=topic_link)
            time.sleep(retry_after)
        except Exception as e:
            print(e)
            time.sleep(10)
            await bot.send_message(chat_id=chat_id, text=topic_link)


bot_data = initialize()
trequest = HTTPXRequest(connection_pool_size=20)
bot = telegram.Bot(token=bot_data['telegram']['token'], request=trequest)
topics = medium.update_articles("topics", "https://medium.com/feed/tag/{}", "../db/medium.json")
retry_after = 5

while True:
    try:
        asyncio.run(send(bot_data['telegram']['channel_id']))
        time.sleep(3600)
    except:
        pass
