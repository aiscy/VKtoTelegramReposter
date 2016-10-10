import aiohttp.web

from endpoints import lc_callback

router = aiohttp.web.UrlDispatcher()
router.add_post('/callback/lc', lc_callback)
