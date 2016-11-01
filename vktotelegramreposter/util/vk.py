import logging
from io import BytesIO

from aiohttp.web import Application
from util import download_file, trim_photo
from util.telegram import send_to_telegram

from config import conf


async def vk_parser(app: Application, task: dict):
    try:
        logging.debug('******New task******\r{}'.format(task))
        tmp_telegram = []
        repost = task.get('copy_history')  # Repost have a similar but not ideantical structure
        if repost:
            task = task['copy_history']
        text = task.get('text')
        if text and conf['KEYS']['IS_LC_TEXT_FILTER_ENABLED']:
            text = text.replace(conf['KEYS']['LC_TEXT_FILTER'], '').strip()
        attachments = task['attachments']
        for obj in attachments:
            obj_type = obj['type']
            if obj_type == 'photo':
                photo = obj['photo']
                photo_url = photo.get('photo_2560',  # TODO Rewrite
                                      photo.get('photo_1280',
                                                photo.get('photo_807',
                                                          photo.get('photo_604',
                                                                    photo.get('photo_130',
                                                                              photo.get('photo_75'))))))
                logging.debug('***Photo URL***\r{}'.format(photo_url))
                photo_bytes = await download_file(app, photo_url)
                photo_object = trim_photo(BytesIO(photo_bytes))
                tmp_telegram.append({'type': obj_type, 'object': photo_object, 'text': text})
            elif obj_type == 'doc':
                doc = obj['doc']
                if doc['ext'] == 'gif':
                    tmp_telegram.append({'type': obj['doc']['ext'], 'object': doc['url'], 'text': text})  # TODO Merge
            else:
                logging.error('###Unsupported type###\r{}'.format(obj))
        await send_to_telegram(app, tmp_telegram, conf['KEYS']['LC_BOT_KEY'], conf['KEYS']['LC_CHANNEL_NAME'])
    except Exception as e:
        logging.exception(e, exc_info=True)
        await app['queue'].put(task)
