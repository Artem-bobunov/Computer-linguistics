
# -*- coding: utf-8 -*-
"""
http://www.torrentino.me/torrents?tags=%D0%BA%D0%BD%D0%B8%D0%B3%D0%B0
http://www.torrentino.me/torrents?page=834&tags=%D0%BA%D0%BD%D0%B8%D0%B3%D0%B0
"""

import requests
from bs4 import BeautifulSoup
from random import choice
import time

from pymongo import MongoClient
client = MongoClient()
db = client.torrent_parser
books = db.books



useragents = open('useragents.txt').read().split('\n')

useragent = {'User-Agent' : choice(useragents)}

def get_html (url, useragent=None, proxies = None):
    """ get the html of pages"""
    r = requests.get(url, headers = useragent, proxies = proxies)
    return r.text

def get_total_pages(html):
    """get total pages"""
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('ul', class_='pagination').find_all('a')[-2].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return total_pages

def get_page_data(html):
    """get the page data"""
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find('div', class_='inner-columns-wrapper').find_all('div', class_='central-right-wrapper-')
    
    for c, item in enumerate(items, 1):
        time.sleep(1)
        try:
            title = item.find('', class_='name').find('a').get('title')
            date = item.find('', class_='').get_text()
            url = item.find('', class_='name').find('a').get('href')
            text = item.find('', class_='').find('a').get('')
            countView = item.find('', class_='').get_text()
            countComment = item.find('', class_='').get_text()
            
            try:
                description_soup = BeautifulSoup(get_html(url, useragent), 'lxml')
                description =  description_soup.find('div', class_='plate description').get_text()
            except:
                description = ''
#                .sort([('score', {'$meta': 'textScore'})])
            i = {
                    'title' : title,
                    'date' : url,
                    'url' : url,
                    'text' : text,
                    'countView' : countView,
                    'countComment' : countComment
                    }
            books.insert_one(i)
            
            print('{} - inserted with size: {}'.format(c, size))
        except Exception as e:
            print('EXCEPT {} with size: {}\n {}'.format(c, size, e))
            continue

url = 'https://v1.ru/'
base_url = 'https://v1.ru/text/gorod/69306460/'
page_part = 'page='
query_part = '&tags=%D0%BA%D0%BD%D0%B8%D0%B3%D0%B0'

total_pages = 100 #get_total_pages(get_html(url, useragent))

for i in range(1, int(total_pages)+1):
    url_gen = base_url + page_part + str(i) + query_part
    html = get_html(url_gen, useragent)
    get_page_data(html)
    


