from aiogram import Dispatcher
from aiogram.utils.markdown import hbold
from datetime import datetime

from create_bot import config, sheduler, dp
from tgbot.middlewares.vk_request import get_news, get_groups, get_friends

import json

async def send_message_to_admin(dp: Dispatcher):
    news_list = await get_news()
    with open('groups.json', encoding='utf-8') as file:
        groups_file_list = json.load(file)
    with open('friends.json', encoding='utf-8') as file:
        friends_file_list = json.load(file)
    for friend in friends_file_list:
        friend_dict = {}
        friend_dict['name'] = f"{friend['first_name']} {friend['last_name']}"
        friend_dict['id'] = friend['id']
        groups_file_list.append(friend_dict)
    for group in groups_file_list:
        group_id = group['id']
        group_name = group['name']
        for news in news_list:
            news_source_id = news['source_id']
            news_text = news['text']
            news_datetime = int(news['datetime']) + 10800
            # news_img_urls = news['img_urls']
            # news_video_prev_urls = news['video_prev_urls']
            # news_audio_urls = news['audio_urls']
            # news_docs_urls = news['docs_urls']
            # news_note_urls = news['notes_urls']
            # news_poll_quest = news['poll_quest']
            # news_market = news['market']
            # news_market_album_title = news['market_album_title']
            # news_pretty_cards = news['pretty_cards']
            # news_event_text = news['event_text']
            news_post_url = news['post_url']

            moscow_time_news = datetime.utcfromtimestamp(news_datetime).strftime("%d-%m-%Y %H:%M:%S")
            if group_id == news_source_id:
                text = [
                    f'НОВЫЙ ПОСТ от {hbold(group_name)}:',
                    '',
                    f'Время поста (Московское): {moscow_time_news}',
                    ''
                ]
                if len(news_text) != 0:
                    text.append(news_text)
                if news_post_url is not None:
                    text.append(news_post_url)
                # if len(news_img_urls) != 0:
                #     text.append(f'Ссылки на фото: {news_img_urls}')
                # if len(news_video_prev_urls) != 0:
                #     text.append(f'Ссылки на превью видео: {news_video_prev_urls}')
                # if len(news_video_prev_urls) != 0:
                #     text.append(f'Ссылки на аудио: {news_audio_urls}')
                # if len(news_video_prev_urls) != 0:
                #     text.append(f'Ссылки на документы: {news_docs_urls}')
                # if len(news_note_urls) != 0:
                #     text.append(f'Ссылки на заметки: {news_note_urls}')
                # if len(news_poll_quest) != 0:
                #     text.append(f'Опросник с вопросом: {hbold(news_poll_quest)}')
                # if len(news_market) != 0:
                #     text.append(f'ТОВАР {news_market["title"]} с описанием {news_market["desc"]} и изображением {news_market["img"]}')
                # if len(news_market_album_title) != 0:
                #     text.append(f'ПОДБОРКА ТОВАРОВ {news_market_album_title}')
                # if len(news_pretty_cards) != 0:
                #     text.append(f'Карточки {news_pretty_cards["title"]}: {news_pretty_cards["url"]}')
                # if len(news_event_text) != 0:
                #     text.append(f'СОБЫТИЕ {hbold(news_event_text)}')


                await dp.bot.send_message(config.tg_bot.admin_ids[0], '\n'.join(text))


async def updater(dp: Dispatcher):
    new_group_dict = []
    new_friend_dict = []
    groups_list = await get_groups()
    friends_list = await get_friends()
    for item in groups_list:
        new_group_dict.append(item)
    with open('groups.json', 'w', encoding='utf-8') as file:
        json.dump(new_group_dict, file, indent=4, ensure_ascii=False)
    for item in friends_list:
        new_friend_dict.append(item)
    with open('friends.json', 'w', encoding='utf-8') as file:
        json.dump(new_friend_dict, file, indent=4, ensure_ascii=False)





def sheduler_jobs():
    sheduler.add_job(send_message_to_admin, 'interval', seconds=20, args=(dp,))
    sheduler.add_job(updater, 'interval', seconds=63, args=(dp,))
    pass