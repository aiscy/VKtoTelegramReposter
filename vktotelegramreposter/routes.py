import aiohttp.web

from endpoints import lc_callback, root

router = aiohttp.web.UrlDispatcher()
router.add_post('/callback/lc', lc_callback)
router.add_get('/', root)