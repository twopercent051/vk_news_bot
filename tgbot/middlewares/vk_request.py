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
            groups_dict['name'] = str(items['name']).replace('<', '_').replace('>', '_')
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
            friends_dict['first_name'] = items['first_name'].replace('<', '_').replace('>', '_')
            friends_dict['last_name'] = items['last_name'].replace('<', '_').replace('>', '_')
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
            notes_urls = []
            market = {}
            pretty_cards = {}
            news_dict = {}
            news_dict['datetime'] = items['date']
            news_dict['source_id'] = items['source_id']
            try:
                news_dict['text'] = items['text']
            except:
                news_dict['text'] = ''
            try:
                post_id = items['post_id']
                source_id = items['source_id']
                post_url = f'https://vk.com/al_feed.php?w=wall{source_id}_{post_id}'
            except:
                post_url = None
            news_dict['post_url'] = post_url
            # try:
            #     attachments = items['attachments']
            # except:
            #     attachments = []
            # for att in attachments:
            #     try:
            #         img_url = att['photo']['sizes'][-1]['url']
            #         img_urls.append(img_url)
            #     except:
            #         pass
            #     try:
            #         video_prev_url = att['video']['image'][-1]['url']
            #         video_prev_urls.append(video_prev_url)
            #     except:
            #         pass
            #     try:
            #         audio_url = att['audio']['url']
            #         audio_urls.append(audio_url)
            #     except:
            #         pass
            #     try:
            #         docs_url = att['doc']['url']
            #         docs_urls.append(docs_url)
            #     except:
            #         pass
            #     try:
            #         notes_url = att['note']['view_url']
            #         notes_urls.append(notes_url)
            #     except:
            #         pass
            #     try:
            #         poll_quest = att['poll']['question']
            #     except:
            #         poll_quest = ''
            #     try:
            #         market['img'] = att['market']['thumb_photo']
            #         market['title'] = att['market']['title']
            #         market['desc'] = att['market']['description']
            #     except:
            #         pass
            #     try:
            #         market_album_title = att['market_album']['title']
            #     except:
            #         market_album_title = ''
            #     try:
            #         pretty_cards['title'] = att['pretty_cards']['title']
            #         pretty_cards['url'] = att['pretty_cards']['link_url']
            #     except:
            #         pass
            #     try:
            #         event_text = att['event']['text']
            #     except:
            #         event_text = ''





            # news_dict['img_urls'] = img_urls
            # news_dict['video_prev_urls'] = video_prev_urls
            # news_dict['audio_urls'] = audio_urls
            # news_dict['docs_urls'] = docs_urls
            # news_dict['notes_urls'] = notes_urls
            # news_dict['poll_quest'] = poll_quest
            # news_dict['market'] = market
            # news_dict['market_album_title'] = market_album_title
            # news_dict['pretty_cards'] = pretty_cards
            # news_dict['event_text'] = event_text
            news_list.append(news_dict)
        return news_list



time_now = (time.time()) + 10800
# print(time_now - (3 * 3600))
# asyncio.run(get_friends())



# print(len('Список групп, на которые вы подписаны ВКонтакте:'))