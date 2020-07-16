import requests
import re
from bs4 import BeautifulSoup

DEAL_OF_THE_DAY_URL = 'https://www.hepsiburada.com/gunun-firsati-teklifi'


class Parser:
    @staticmethod
    def _get_page_content():
        r = requests.get(DEAL_OF_THE_DAY_URL)
        return r.text

    @classmethod
    def parse(cls, content):
        soup = BeautifulSoup(content, 'html.parser')
        all_divs = soup.find_all('a', class_='deal-of-the-day-item')
        return [cls._parse_dotd_item(dotd) for dotd in all_divs]

    @classmethod
    def _parse_dotd_item(cls, dotd_item):
        data = {
            'name': cls._parse_name(dotd_item),
            'link': cls._parse_link(dotd_item),
            'old_price': cls._parse_old_price(dotd_item),
            'discount_amount': cls._parse_discount(dotd_item),
            'current_price': cls._parse_current_price(dotd_item),
            'image': cls._parse_img(dotd_item),
            'bucket_value': cls._parse_bucket_value(dotd_item)
        }
        return data

    @staticmethod
    def _parse_name(dotd):
        return dotd.find('h3', class_='deal-of-the-day-name').get_text()

    @staticmethod
    def _parse_link(dotd):
        return f'https://www.hepsiburada.com{dotd["href"]}'

    @staticmethod
    def _parse_old_price(dotd):
        return dotd.find('del', class_='price old product-old-price').get_text()

    @staticmethod
    def _parse_discount(dotd):
        return f"{dotd.find('span', class_='discount-content').find('span').get_text()}%"

    @staticmethod
    def _parse_current_price(dotd):
        try:
            return dotd.find('span', class_='price product-price').get_text()
        except AttributeError:
            return dotd.find('span', class_='price old product-old-price').get_text()

    @staticmethod
    def _parse_bucket_value(dotd):
        bucket_value_obj = dotd.find('div', class_='price-value')
        if bucket_value_obj:
            bucket_value = bucket_value_obj.get_text().strip()
            parsed_value = re.match(r'(.+?)\s', bucket_value).group(1)
            return f"{parsed_value} TL"
        return ''

    @staticmethod
    def _parse_img(dotd):
        return dotd.find('img').get('src')

    @classmethod
    def run(cls):
        content = cls._get_page_content()
        return cls.parse(content)
