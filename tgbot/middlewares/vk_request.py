import aiohttp
import asyncio
import json
import time
from datetime import datetime

from create_bot import config

token = config.misc.vk_token


async def get_groups():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.vk.com/method/groups.get?extended=1&access_token={token}&v=5.131') as resp:
            responce = await resp.read()
        data = json.loads(responce)
        groups_list = []
        for items in data['response']['items']:
            groups_dict = {}
            groups_dict['id'] = int(items['id']) * (-1)
            groups_dict['name'] = items['name']
            groups_list.append(groups_dict)
        return groups_list
        # print(groups_list)



async def get_friends():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.vk.com/method/friends.get?fields=nickname&access_token={token}&v=5.131') as resp:
            responce = await resp.read()
        data = json.loads(responce)
        friends_list = []
        for items in data['response']['items']:
            friends_dict = {}
            friends_dict['id'] = int(items['id'])
            friends_dict['first_name'] = items['first_name']
            friends_dict['last_name'] = items['last_name']
            friends_list.append(friends_dict)
        return friends_list
        # print(friends_list)



async def get_news():
    async with aiohttp.ClientSession() as session:
        start_time = int(time.time()) - 21
        async with session.get(f'https://api.vk.com/method/newsfeed.get?start_time={start_time}&access_token={token}&v=5.131') as resp:
            responce = await resp.read()
        data = json.loads(responce)
        news_list = []
        for items in data['response']['items']:
            img_urls = []
            video_prev_urls = []
            docs_urls = []
            audio_urls = []
            news_dict = {}
            news_dict['datetime'] = items['date']
            news_dict['source_id'] = items['source_id']
            try:
                news_dict['text'] = items['text']
            except:
                news_dict['text'] = ''
            try:
                attachments = items['attachments']
            except:
                attachments = []
            for att in attachments:
                try:
                    img_url = att['photo']['sizes'][-1]['url']
                    img_urls.append(img_url)
                except:
                    pass
                try:
                    video_prev_url = att['video']['image'][-1]['url']
                    video_prev_urls.append(video_prev_url)
                except:
                    pass
                try:
                    audio_url = att['audio']['url']
                    audio_urls.append(audio_url)
                except:
                    pass
                try:
                    docs_url = att['doc']['url']
                    docs_urls.append(docs_url)
                except:
                    pass

            news_dict['img_urls'] = img_urls
            news_dict['video_prev_urls'] = video_prev_urls
            news_dict['audio_urls'] = audio_urls
            news_dict['docs_urls'] = docs_urls
            news_list.append(news_dict)
        return news_list



time_now = (time.time()) + 10800
# print(time_now - (3 * 3600))
# asyncio.run(get_friends())



time_good = datetime.utcfromtimestamp(time_now).strftime("%d-%m-%Y %H:%M:%S")
print(time_good)