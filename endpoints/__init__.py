import aiohttp.web
from endpoints.lc import lc_callback

async def root(request):
    return aiohttp.web.HTTPFound('https://www.youtube.com/watch?v=V4MF2s6MLxY')