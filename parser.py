import collections
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb')

ParseResult = collections.namedtuple(
    'ParseResult', (
        'brandName',
        'goodsName',
        'url',
    )
)

class Client:

    def __init__(self):  #создание объекта Client, в котором создается сессия, + headers браузера
        self.session = requests.Session()
        self.session.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
                                'Accept=Language': 'ru',}
        self.result = []
    
    def load_page(self):  #загрузка сессией страницы по данному url
        url = 'https://www.wildberries.ru/catalog/muzhchinam/odezhda?sort=popular&page=1'
        res = self.session.get(url=url)  #здесь ответ(responce) на запрос
        res.raise_for_status()  #метод возвращающий код ответа http(200 404 500 и тд)
        return res.text         #возврат текста в html формате 

    def parse_page(self, text:str):  #парсинг страницы, на входе bs обрабатывает текст полученный из requests
        soup = BeautifulSoup(text, 'lxml')
        container = soup.select('div.product-card.j-card-item') #отбор контента по классам css
        for block in container:   # для каждого блока контейнера
            self.parse_block(block=block)  #происходит вывод в консоль + отделение горизонтальной чертой из знаков ========

    def parse_block(self, block):
        # logger.info(block)
        # logger.info('='*100)
        
        urlblock = block.select_one('a.product-card__main.j-open-full-product-card')
        if not urlblock:
            logger.error('no url block')
        url = urlblock.get('href')
        if not url:
            logger.error('no href')
        url ='https://www.wildberries.ru'+url

        nameblock = block.select_one('div.product-card__brand-name')
        if not nameblock:
            logger.error(f'no name_block block on {url}')

        brandname = nameblock.select_one('strong.brand-name')
        if not brandname:
            logger.error(f'no brandname on {url} ')        
        brandname = brandname.text
        brandname = brandname.replace('/', '').strip()

        goodsname = nameblock.select_one('span.goods-name')
        if not goodsname:
            logger.error(f'no goodsname on {url}')
        goodsname = goodsname.text
        
        self.result.append(ParseResult(
            url=url,
            brandName=brandname,
            goodsName=goodsname
        ))

        logger.debug('%s, %s, %s', url, brandname, goodsname)
        logger.debug('-'*100)



    def run(self):  #основная функция запуска парсера 1) получает текст 
        text = self.load_page()
        self.parse_page(text=text)
        logger.info(f'Получено {len(self.result)}')

if __name__ == '__main__':
    parser = Client()
    parser.run()
        



# url = 'https://www.acer.com/ac/ru/RU/content/support-product/7572?b=1'
# responce = requests.get(url)
# soup = BeautifulSoup(responce.text, 'lxml')
# print(type(soup))
# p = soup.find_all('p')
# for el in p:
#     print(el)


