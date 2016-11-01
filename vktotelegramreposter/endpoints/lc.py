import logging

from aiohttp.web import Request, Response
from aiohttp.web_exceptions import HTTPBadRequest

from config import conf


async def lc_callback(request: Request) -> Response:
    event = await request.json()  # type: dict
    logging.debug('NEW EVENT:\r{}'.format(event))
    try:
        event_type = event['type']
    except KeyError:
        return HTTPBadRequest()
    if event_type == 'confirmation':
        return Response(text=conf['KEYS']['LC_KEY'])
    elif event_type == 'wall_post_new':
        await request.app['queue'].put(event['object'])
        return Response(text='ok')
    else:
        return Response()
