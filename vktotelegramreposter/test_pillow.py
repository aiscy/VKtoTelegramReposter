from PIL import Image, ImageChops


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        return None

im = Image.open('3.jpg')
im = trim(im)
im.save('4.jpg')


# def main():
#     im = Image.open('cM4jhxajAE8.jpg')
#     invert_im = list(ImageOps.invert(im).getbbox())
#     invert_im[0] += 15
#     invert_im[2] -= 15
#     img = im.crop(invert_im).tobytes()
#     print(img)
#
# if __name__ == '__main__':
#     main()
