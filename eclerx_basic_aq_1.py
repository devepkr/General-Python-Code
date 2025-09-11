import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://quotes.toscrape.com/'
product_url = base_url
file_name = 'data.csv'


all_quotes = []

pagination_cnt = 0
while True:
    if pagination_cnt == 2:
        break
    res = requests.get(product_url)
    print(f"Scraping: {product_url}")
    soup = BeautifulSoup(res.content, 'lxml')

    quotes = soup.select('div[class="quote"]')
    for item in quotes:
        quote = item.select_one('[itemprop="text"]').text
        author = item.select_one('[itemprop="author"]').text
        tag_elements = item.select('div.tags a.tag')
        tags = ', '.join([tag.text for tag in tag_elements])

        quote_data = {"Quote": quote, "Author": author, "Tags": tags}
        all_quotes.append(quote_data)

    # Pagination
    next_button = soup.select_one('ul.pager li.next a')
    if next_button:
        next_url = next_button.get('href')
        product_url = urljoin(product_url, next_url)
        pagination_cnt += 1
    else:
        break


df = pd.DataFrame(all_quotes)
df.to_csv(file_name, index=False, quoting=1)

print(f"Data saved to {file_name}")
