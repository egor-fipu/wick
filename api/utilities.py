import requests
from PIL import Image, ImageOps, ImageDraw, ImageFont
from django.template.loader import render_to_string


def watermark_text(input_image, output_image_path, text, pos):
    photo = Image.open(input_image)
    photo = ImageOps.exif_transpose(photo)

    fixed_height = 500
    width_size = int(fixed_height * photo.width / photo.height)
    photo = photo.resize((width_size, fixed_height), Image.ANTIALIAS)

    drawing = ImageDraw.Draw(photo)
    black = (3, 8, 12)
    font = ImageFont.truetype('arial.ttf', size=40)
    drawing.text(pos, text, fill=black, font=font)
    photo.save(output_image_path)


def watermark_photo(input_image, output_image_path, pos):
    base_image = Image.open(input_image)
    base_image = ImageOps.exif_transpose(base_image)
    watermark = Image.open('users/media/watermark.png')

    fixed_height = 500
    width_size = int(fixed_height * base_image.width / base_image.height)
    base_image = base_image.resize((width_size, fixed_height), Image.ANTIALIAS)
    width, height = (width_size, fixed_height)

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, pos, mask=watermark)
    transparent.save(output_image_path)


def send_like_email(follower, following):
    context = {
        'follower': follower,
        'following': following
    }
    subject = render_to_string(
        'emails/send_like_subject.txt',
        context
    )
    body_text = render_to_string(
        'emails/send_like_body.txt',
        context
    )
    follower.email_user(subject, body_text)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_coord(request):
    ip = get_client_ip(request)
    if ip == '127.0.0.1':
        ip = ''
    ip_response = requests.get('http://ipwhois.app/json/' + ip)
    ipgeolocation = ip_response.json()
    latitude = ipgeolocation.get('latitude')
    longitude = ipgeolocation.get('longitude')
    return latitude, longitude
