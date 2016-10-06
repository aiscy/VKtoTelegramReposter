import asyncio
import logging
import pathlib
from aiohttp import web

from middlewares import setup_middlewares
from routes import setup_routes
from config import conf

PROJ_ROOT = pathlib.Path(__file__).parent


async def init(loop):
    app = web.Application(loop=loop)

    setup_routes(app, PROJ_ROOT)
    setup_middlewares(app)

    host, port = conf['HOST'], conf['PORT']
    return app, host, port


def main():
    logging.basicConfig(level=conf['LOGGER_LEVEL'])

    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
