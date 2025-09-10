
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_books():
    sess = requests.Session()
    base_url = "https://books.toscrape.com/"
    # base_url = "http://quotes.toscrape.com/"
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
        if pagination_cnt == 2:
            print('Break to pagination.')
            break
        res = sess.get(product_url, headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        print('product -- url: ', product_url)
        print(res.status_code)

        card_section = soup.select('article[class="product_pod"]')
        for card in card_section:
            print(card)
            price = card.select_one('p[class="price_color"]').next_element
            print(price)

        next_button = soup.select_one('li[class="next"] a')
        if next_button:
            next_url = next_button.get('href')
            product_url = urljoin(product_url, next_url)
            pagination_cnt += 1
        else:
            print('No more pages.')
            break

scrape_books()
