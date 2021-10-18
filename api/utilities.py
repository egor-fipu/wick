import requests
from django.template.loader import render_to_string

from users.models import Follow


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


def check_follow(follower, following):
    if not Follow.objects.filter(follower=following,
                                 following=follower).exists():
        return False
    send_like_email(follower=follower, following=following)
    send_like_email(follower=following, following=follower)
    data = {
        'message': f'Вы тоже понравились {following.first_name}! '
                   f'Почта участника: {following.email}'
    }
    return data


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
