import collections, os, csv
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb')

ParseResult = collections.namedtuple(
    'ParseResult', (
        'name',
        'price',
        'url',
    )
)

HEADERS = (
    'Товар',
    'Цена',
    'Ссылк',
    )

class Client:

    def __init__(self):  #создание объекта Client, в котором создается сессия, + headers браузера
        self.session = requests.Session()
        self.session.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
                                'Accept=Language': 'ru',}
        self.result = []
    
    def load_page(self, page):  #загрузка сессией страницы по данному url
        url = f'https://santehgas.ru/vodosnabzhenie/?page={page}'
        res = self.session.get(url=url)  #здесь ответ(responce) на запрос
        res.raise_for_status()  #метод возвращающий код ответа http(200 404 500 и тд)
        return res.text         #возврат текста в html формате 

    def parse_page(self, text:str):  #парсинг страницы, на входе bs обрабатывает текст полученный из requests
        soup = BeautifulSoup(text, 'lxml')
        container = soup.select('div.product.flexdiscount-product-wrap') #отбор контента по классам css
        for block in container:   # для каждого блока контейнера
            self.parse_block(block=block)  #происходит вывод в консоль + отделение горизонтальной чертой из знаков ========

    def parse_block(self, block):
        # logger.info(block)
        # logger.info('='*100)
        
        urlblock = block.select_one('a')
        if not urlblock:
            logger.error('no url block')
        url = urlblock.get('href')
        if not url:
            logger.error('no href')
        url = 'https://santehgas.ru' + url
        name = urlblock.get('title')

        priceblock = block.select_one('span')
        if not priceblock:
            logger.error('no price block')
        price = priceblock.text

        

        # nameblock = block.select_one('div.product-card__brand-name')
        # if not nameblock:
        #     logger.error(f'no name_block block on {url}')

        # brandname = nameblock.select_one('strong.brand-name')
        # if not brandname:
        #     logger.error(f'no brandname on {url} ')        
        # brandname = brandname.text
        # brandname = brandname.replace('/', '').strip()

        # goodsname = nameblock.select_one('span.goods-name')
        # if not goodsname:
        #     logger.error(f'no goodsname on {url}')
        # goodsname = goodsname.text
        
        self.result.append(ParseResult(
            url=url,
            price=price,
            name=name,
        ))

        logger.debug('%s, %s, %s', url, name)
        logger.debug('-'*100)

    def save_result(self, page):
        path = os.path.abspath(os.curdir) + '/santehpars.csv'
        with open(path, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL) #обращение к модули записи в css файл
            writer.writerow(HEADERS) # метод 'записать строку(хедеры)
            for item in self.result:
                writer.writerow(item)



    def run(self, page):  #основная функция запуска парсера 1) получает текст 
        text = self.load_page(page)
        self.parse_page(text=text)
        logger.info(f'Получено {len(self.result)}')
        self.save_result(page)

if __name__ == '__main__':
    parser = Client()
    for i in range(3):
        parser.run(i)
        



# url = 'https://www.acer.com/ac/ru/RU/content/support-product/7572?b=1'
# responce = requests.get(url)
# soup = BeautifulSoup(responce.text, 'lxml')
# print(type(soup))
# p = soup.find_all('p')
# for el in p:
#     print(el)





# url = 'https://www.acer.com/ac/ru/RU/content/support-product/7572?b=1'
# responce = requests.get(url)
# soup = BeautifulSoup(responce.text, 'lxml')
# print(type(soup))
# p = soup.find_all('p')
# for el in p:
#     print(el)

#/home/nikita_listopadov/bs4_parser




        







