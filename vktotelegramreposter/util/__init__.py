from PIL import Image, ImageChops
from io import BytesIO

from aiohttp.client import ClientSession


async def download_file(app, url):
    async with ClientSession(loop=app.loop) as session:
        async with session.get(url) as response:
            return await response.read()


def trim_photo(image_object: BytesIO) -> BytesIO:  # TODO Rewrite
    im = Image.open(image_object)
    im_format = Image.MIME[im.format]
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)
    obj = BytesIO()
    im.save(obj, 'jpeg')
    return obj
