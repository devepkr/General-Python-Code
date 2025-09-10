import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

base_url = 'https://books.toscrape.com/'

def get_response():
    res = requests.session()
    url = 'https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html'
    res_url = res.get(url)
    soup = BeautifulSoup(res_url.content, 'lxml')
    return soup

def extract_data():
    soup = get_response()
    title_selector = soup.select_one('div[class="col-sm-6 product_main"]').decode_contents()
    title_pattern = re.compile(r'<h1>([^"]+)</h1>')
    title =  title_pattern.search(title_selector).group(1)

    price_selector = soup.select_one('div[class="col-sm-6 product_main"]').decode_contents()
    price_pattern = re.compile('class="[^"]+">£(.*?)</p>')
    price = price_pattern.search(price_selector).group(1)

    upc_selector = soup.select_one('table[class="table table-striped"]').decode_contents()
    upc_pattern = re.compile(r'<th>UPC</th><td>(.*?)</td>')
    upc = upc_pattern.search(upc_selector).group(1)

    is_stock = soup.select_one('p[class="instock availability"]').decode_contents()
    is_stock_pattern = re.compile(r'(\d+)\s+available')
    stock = is_stock_pattern.search(is_stock).group(1)

    image_tag = soup.select_one('#product_gallery img').get('src')
    image_url = urljoin(base_url,image_tag)

    rating_tag = soup.select_one('p.star-rating')
    rating_class = rating_tag['class']
    rating_group = rating_class[1]
    rating_map = {'One': 1, 'Two': 2, 'Three': 3,'Four': 4, 'Five': 5}
    star_rating = rating_map.get(rating_group, 0)

    book_data = {
        "title": title,
        "price": f"£{price}",
        "upc": upc,
        "in_stock": int(stock),
        'Images' : image_url,
        "star_rating": star_rating
    }

    print(book_data)

extract_data()