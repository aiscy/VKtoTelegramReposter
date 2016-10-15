import logging
# from aiohttp import ClientSession
from aiohttp.web import Request, Response, HTTPNotImplemented
from aiotg import Bot
# from aiovk.api import API
# from aiovk.sessions import TokenSession
# from json import dumps
from config import conf

def error_log(json: dict):
    logging.error('Unexpected result in {}'.format(json))

async def lc_callback(request: Request):
    json = await request.json()
    if json['type'] == 'confirmation':
        key = conf['KEYS']['LC_KEY']
        return Response(text=key)
    elif json['type'] == 'wall_post_new':
        tg_bot = Bot(api_token=conf['KEYS']['LC_BOT_KEY'])
        tg_channel = tg_bot.channel(conf['KEYS']['LC_CHANNEL_NAME'])
        text = json['object'].get('text', '')
        if text and conf['KEYS']['IS_LC_TEXT_FILTER_ENABLED']:
            text = text.replace(conf['KEYS']['LC_TEXT_FILTER'])
        for obj in json['object']['attachments']:
            if obj['type'] == 'photo':
                photo = obj['photo']
                await tg_channel.send_photo(photo.get('photo_2560', photo.get('photo_1280', photo.get('photo_807', photo.get('photo_604', photo.get('photo_130', photo.get('photo_75')))))), text)
            elif obj['type'] == 'doc':
                doc = obj['doc']
                if doc['ext'] == 'gif':
                    await tg_channel.send_video(doc['url'], text)
                else:
                    error_log(json)
            else:
                error_log(json)
            # elif obj['type'] == 'video':
            #     video = obj['video']
            #     logging.debug(video)
            #     video_id = video['id']
            #     video_owner = video['owner_id']
                # access_token = video['access_key']
                # vk_session = TokenSession()
                # vk_api = API(vk_session)
                # logging.info()
                # video_info = await vk_api.video.get(videos='{}_{}'.format(video_owner, video_id))
                # await tg_channel.send_document(video_info['items'][0]['player'].replace('?__ref=vk.api', ''))
                # await tg_channel.send_video(video_info['items'][0]['player'], text)
                # async with ClientSession() as session:
                #     async with session.post('https://api.vk.com/method/video.get', data=dict(v='5.57',
                #                            videos='{}_{}_{}'.format(video_owner, video_id, access_token))) as resp:
                #         logging.info(await resp.text())

        return Response(text='ok')
    else:
        error_log(json)
        raise HTTPNotImplemented()
