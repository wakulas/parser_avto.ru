import requests
from bs4 import BeautifulSoup
import csv


HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/95.0.4638.69 Safari/537.36', 'accept': '*/*'}
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    r.encoding = 'utf-8'
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='ListingPagination__page')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='ListingItem__main')
    cars = []
    try:
        for item in items:
            cars.append({
                'title': item.find('h3', class_='ListingItemTitle').get_text(strip=True),
                'link': item.find('a', class_='Link ListingItemTitle__link').get('href'),
                'price': item.find('div', class_='ListingItemPrice').get_text(),
                'city': item.find('span', class_='MetroListPlace__regionName').get_text(),
                'specifications': item.find('div', class_='ListingItemTechSummaryDesktop__cell').get_text()
            })
    except AttributeError:
        print('ничего нет')
    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv .writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена', 'Город', 'Характеристики'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price'], item['city'], item['specifications']])


def parse():
    URL = input('Введите URL: ')
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
    #        cars = get_content(html.text)
        save_file(cars, FILE)
        print(f'Получено {len(cars)} автомобилей')

    else:
        print('error!!1')


parse()
