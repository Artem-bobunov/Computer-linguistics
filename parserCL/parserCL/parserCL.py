#библиотека для запросов
import requests
from bs4 import BeautifulSoup
from random import choice 
import urllib.request

userparsers = open('userparser.txt').read().split('\n')

userparser = {'Userparser': choice(userparsers)}
# полчуение html страницы
def get_html (url, userparser=None, proxies=None):
    r=requests.get(url,headers=userparser,proxies=None)
    return r.text
#Получение всех страници
def get_total_pages(html):
    soup = BeautifulSoup(html,'lxml')
    pages = soup.find('div', class_='G1acv' ).find_all('a')[-1].get('href')
    result='https://v1.ru/'+ pages 
    return result
def get_page_data(html):
   
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find('div', class_='BXer').find_all('article', class_='MJaz5')
    for c, item in enumerate(items, 1):
        #time.sleep(1)
        try:
            title = item.find('div', class_='MJaz7').find('a').get('title')
            url = item.find('div', class_='MJaz7').find('a').get('href') 
            datetimes = item.find('div', class_='MJlr').find('time').get('datetime')
            count_view = item.find('div', class_='LVaxt').find('span').get_text()
            #проверка на наличие комментариев
            if item.find('a', class_='LVcp LVbn') != None:
                count_comment = item.find('a', class_='LVcp LVbn').find('span', class_='LVcl').get_text()
            else: 
                count_comment = None
            #проверка на наличие видео
            #iFrames=[] # qucik bs4 example
            #for iframe in soup("iframe"):
               #iFrames.append(soup.iframe.extract())

            if BeautifulSoup(get_html('https:/'+'/v1.ru/'+ url), 'lxml').find('div', class_='ERsn') != None:
                video = BeautifulSoup(get_html('https:/'+'/v1.ru/'+ url), 'lxml').find('iframe')
            else: 
                video = None
            #достаем полностью текст 
            text_url=''
            for i in BeautifulSoup(get_html('https:/'+'/v1.ru/'+ url), 'lxml').find_all('div', class_='LPawp'):
                for j in i.find_all('p'):
                    text_url+=j.get_text()
            i = {
                    'title' : title,
                    'url': url,
                    'text': text_url,
                    'datetime' : datetimes,
                    'count_comment': count_comment,
                    'count_view': count_view           
                 }
            print("Ссылка на видео:",video)
            print("Количество просмотров:" + count_view)
            print("Количество комментариев:", count_comment)
            print("Текст записи:"+ text_url)
            print("Название новости:"+title)
            print("Дата публикации:"+ datetimes)
            print('https:/'+'/v1.ru/'+ url)
        except Exception as e:
            #Выводит ошибку
            print(e)
            print('EXCEPT {} \n'.format(c,e))
            continue


url = 'https://v1.ru/'
base_url = 'https://v1.ru/text/?'
page_part = 'page='


total_pages = 1 

for i in range(1, int(total_pages)+1):
    url_gen = base_url + page_part + str(i) 
    html = get_html(url_gen, userparser)
    get_page_data(html)







