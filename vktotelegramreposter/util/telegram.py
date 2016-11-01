import logging

from telepot.aio import Bot


async def send_to_telegram(app, obj_list, token, channel):
    logging.debug('Telegram object:\r{}'.format(obj_list))
    bot = Bot(token=token, loop=app.loop)
    for obj in obj_list:
        obj_type = obj['type']
        if obj_type == 'photo':
            await bot.sendPhoto(channel, ('1.jpg', obj['object'].getvalue()), obj.get('text'))
        elif obj_type == 'gif':
            await bot.sendVideo(channel, obj['object'], obj.get('text'))
