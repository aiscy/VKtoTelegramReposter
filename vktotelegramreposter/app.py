import asyncio
from logging.config import dictConfig

from aiohttp import web, ClientSession
from aiohttp.web import Application
from routes import router
from util.vk import vk_parser

from config import conf


async def listen_queue(app: Application):
    try:
        while True:
            task = await app['queue'].get()
            await vk_parser(app, task)
    except asyncio.CancelledError:
        pass


async def start_background_tasks(app: Application):
    app['client_session'] = ClientSession()
    app['queue'] = asyncio.Queue(loop=app.loop)
    app.loop.create_task(listen_queue(app))


async def cleanup_background_tasks(app: Application):
    pass


async def init(loop):
    app = web.Application(loop=loop, router=router, debug=True)
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    host, port = conf['HOST'], conf['PORT']
    return app, host, port


def main():
    dictConfig(conf['LOGGING_CONF'])
    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
