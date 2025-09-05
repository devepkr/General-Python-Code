
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
sess = requests.Session()
base_url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"
product_url = base_url

headers = {
    'priority': 'u=0, i',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}
pagination_cnt = 1
while True:
    if pagination_cnt > 3:
        print('Break to pagination.')
        # break
    res = sess.get(product_url, headers=headers)
    soup = BeautifulSoup(res.content, 'lxml')
    print('product -- url: ', product_url, pagination_cnt)
    print(res.status_code)

    card_section = soup.select('article[class="product_pod"]')
    for card in card_section:
        price = card.select_one('p[class="price_color"]')
        print(price)

    next_button = soup.select_one('a[class="page-link next"]')
    if next_button:
        next_url = next_button.get('href')
        product_url = urljoin(product_url, next_url)
        pagination_cnt += 1
    else:
        print('No more pages.')
        break

