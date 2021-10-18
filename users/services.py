from PIL import Image, ImageOps


def watermark_image(image_path):
    img = Image.open(image_path)
    img = ImageOps.exif_transpose(img)

    fixed_height = 500
    width_size = int(fixed_height * img.width / img.height)
    img = img.resize((width_size, fixed_height), Image.ANTIALIAS)
    width, height = (width_size, fixed_height)

    watermark = Image.open('users/media/watermark.png')
    watermark.thumbnail((150, 100))
    mark_width, mark_height = watermark.size
    paste_mask = watermark.split()[3].point(lambda i: i * 50 / 100)
    x = width - mark_width - 10
    y = height - mark_height - 10
    img.paste(watermark, (x, y), mask=paste_mask)
    img.save(image_path)
