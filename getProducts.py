from selenium.webdriver import Chrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from webdriver_manager.utils import ChromeType
from tqdm import tqdm
from urllib.parse import quote, quote_plus
from multiprocessing import Process, Queue
import concurrent.futures


class Product():
    def __init__(self, name='', img='', url=''):
        self.name = name
        self.img = img
        self.url = url

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def get_products_myntra(term):
    term = term.replace('color', '')
    term = term.replace(' ', '-')
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = Chrome(ChromeDriverManager(
        chrome_type=ChromeType.GOOGLE).install(), options=op)
    print('Loading webpage...')

    driver.get('https://www.myntra.com/{}'.format(term))
    res = driver.find_elements_by_class_name('product-base')
    products = []

    for r in tqdm(res[:10]):

        name = "{} {}".format(r.find_element_by_tag_name(
            'h3').text, r.find_element_by_tag_name('h4').text)
        img = r.find_element_by_tag_name('img').get_attribute('src')
        url = r.find_element_by_tag_name('a').get_attribute('href')

        products.append(Product(name, img, url))

    driver.close()
    return products


def get_products_flipkart(term):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = Chrome(ChromeDriverManager(
        chrome_type=ChromeType.GOOGLE).install(), options=op)
    print('Loading webpage...')

    driver.get('https://www.flipkart.com/search?q={}'.format(quote(term)))
    res = driver.find_elements_by_css_selector("._3O0U0u")
    products = []

    for r in tqdm(res[:10]):
        name = '{} {}'.format(r.find_element_by_class_name(
            '_2B_pmu').text, r.find_element_by_class_name('_2mylT6').text)
        img = r.find_element_by_tag_name('img').get_attribute('src')
        url = r.find_element_by_class_name('_2mylT6').get_attribute('href')
        products.append(Product(name, img, url))
    driver.close()
    return products


def get_products_amazon(term):

    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = Chrome(ChromeDriverManager(
        chrome_type=ChromeType.GOOGLE).install(), options=op)
    print('Loading webpage...')

    driver.get('https://www.amazon.in/s?k={}'.format(quote(term)))

    res = driver.find_elements_by_css_selector(".sg-col-inner")
    products = []

    # skip  first 8 elements as they are not seacrh results
    for r in tqdm(res[4:14]):

        name = '{} {}'.format(r.find_element_by_css_selector('.a-size-base-plus.a-color-base').text,
                              r.find_element_by_css_selector('.a-size-base-plus.a-color-base.a-text-normal').text)
        img = r.find_element_by_tag_name('img').get_attribute('src')
        url = r.find_element_by_tag_name('a').get_attribute('href')

        products.append(Product(name, img, url))
    driver.close()
    return products


def get_all_products(term):
    prod = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(get_products_amazon, term)
        f2 = executor.submit(get_products_flipkart, term)
        f3 = executor.submit(get_products_myntra, term)
        prod = [f1.result(), f2.result(), f3.result()]

    return {'Amazon': [p.__dict__ for p in prod[0]], 'Flipkart': [p.__dict__ for p in prod[1]],  'Myntra': [p.__dict__ for p in prod[2]], }
