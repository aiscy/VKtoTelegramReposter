import asyncio
from logging.config import dictConfig
from aiohttp import web

from routes import router
from config import conf


async def init(loop):
    app = web.Application(loop=loop, router=router, debug=True)
    host, port = conf['HOST'], conf['PORT']
    return app, host, port


def main():
    dictConfig(conf['LOGGING_CONF'])
    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
