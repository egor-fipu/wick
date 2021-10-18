import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from products.models import Category, Notebook


class Command(BaseCommand):

    def handle(self, *args, **options):

        category, status = Category.objects.get_or_create(title='Ноутбуки')

        url = 'https://www.citilink.ru/catalog/noutbuki/'
        response = requests.get(url)

        obj_list = []
        page_number = 1

        while response.status_code == 200 and page_number != 3:

            soup = BeautifulSoup(response.text, 'html.parser')

            for c in soup.find_all(
                    'div', class_='ProductCardHorizontal__image-block'):
                price = c.parent.attrs.get('data-price')
                link = c.find('a')['href']
                name = c.find('img')['alt']
                image = c.find('source')['srcset']

                try:
                    obj = Notebook(
                        name=name,
                        price=float(price.replace(' ', '')),
                        link='https://www.citilink.ru' + link,
                        image=image,
                        category=category
                    )
                    obj_list.append(obj)
                except Exception as error:
                    print(f'{error} -Ошибка создания объекта модели')

            page_number += 1
            url = f'https://www.citilink.ru/catalog/noutbuki/?p={page_number}'
            response = requests.get(url)

        try:
            Notebook.objects.bulk_create(obj_list)
        except Exception as error:
            print(f'{error} -Ошибка добавления данных в БД')

        self.stdout.write(self.style.SUCCESS('Данные успешно добавлены в БД'))
