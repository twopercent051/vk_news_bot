from aiogram import Dispatcher
from aiogram.utils.markdown import hbold
from datetime import datetime

from create_bot import config, sheduler, dp
from tgbot.middlewares.vk_request import get_news

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
            news_img_urls = news['img_urls']
            news_video_prev_urls = news['video_prev_urls']
            news_audio_urls = news['audio_urls']
            news_docs_urls = news['docs_urls']
            moscow_time_news = time_good = datetime.utcfromtimestamp(news_datetime).strftime("%d-%m-%Y %H:%M:%S")
            if group_id == news_source_id:
                text = [
                    f'НОВЫЙ ПОСТ от {hbold(group_name)}:',
                    '',
                    news_text,
                    '',
                    f'Время поста (Московское): {moscow_time_news}'
                ]
                # if len(news_img_urls) != 0:
                #     text.append(f'Ссылки на фото: {news_img_urls}')
                # if len(news_video_prev_urls) != 0:
                #     text.append(f'Ссылки на превью видео: {news_video_prev_urls}')
                # if len(news_video_prev_urls) != 0:
                #     text.append(f'Ссылки на аудио: {news_audio_urls}')
                # if len(news_video_prev_urls) != 0:
                #     text.append(f'Ссылки на документы: {news_docs_urls}')

                await dp.bot.send_message(config.tg_bot.admin_ids[0], '\n'.join(text))





def sheduler_jobs():
    sheduler.add_job(send_message_to_admin, 'interval', seconds=20, args=(dp,))
    pass