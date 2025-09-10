import os
import time
import random
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup





logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('run.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


collect_product_data = []

class ZeptoData:
    def __init__(self, URL):
        self.url = URL
        self.user_agent_list = [
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'},
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/114.0.1823.51 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/113.0'},
            {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/113.0.1774.57 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/112.0'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
        ]

        self.header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',

        }

    def get_response(self):
        selected_user_agent = random.choice(self.user_agent_list)
        headers = {**self.header, **selected_user_agent}
        logger.info(f"Fetching URL: {self.url}")
        logger.info(f"Using headers: {headers}")
        sess = requests.session()

        try:
            res = sess.get(self.url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.content, 'lxml')
            return soup
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch {self.url}: {e}")
            return None

    def extract_data(self):
        pk = self.get_response()
        if not pk:
            logger.warning(f"Skipping URL due to failed request: {self.url}")
            return


        title = ''
        try:
            title = pk.select_one('[class="rounded-2xl"] h1').text.strip()
            print(f"Title: {title}")
        except (AttributeError, TypeError) as e:
            logger.error(f"Error extracting title for {self.url}: {e}")

        price = ''
        try:
            price = pk.select_one('p[class="flex items-center justify-center gap-2"]').text.strip().replace('₹', '')
            print(f"Price: {price}")
        except (AttributeError, TypeError) as e:
            logger.error(f"Error extracting price for {self.url}: {e}")

        sell_price = ''
        try:
            sell_price = pk.select_one('[class="rounded-2xl"] [class="line-through font-bold"]').text.strip().replace('₹', '')
            print(f"Sell Price: {sell_price}")
        except (AttributeError, TypeError) as e:
            logger.error(f"Error extracting sell price for {self.url}: {e}")

        specs = ''
        try:
            attr_name = [name.text.strip() for name in pk.select('[id="productHighlights"] h3')]
            attr_value = [value.text.strip() for value in pk.select('[id="productHighlights"] p')]
            specs = [{name_li: values_li} for name_li, values_li in zip(attr_name, attr_value)]
            print(f"Specs: {specs}")
        except (AttributeError, TypeError) as e:
            logger.error(f"Error extracting specs for {self.url}: {e}")

        product = {
            'URL' : self.url,
            'Title': title,
            'Price': price,
            'Sell_price': sell_price,
            'Specs': specs
        }
        logger.info(f"Extracted: {product}")
        collect_product_data.append(product)


if __name__ == "__main__":
    logger.info("Starting Zepto web scraping")
    url_list = [
        'https://www.zepto.com/pn/tata-sampann-unpolished-moong-dal/pvid/cfc5e58e-1b02-4f88-9ae4-85630c217570',
        'https://www.zeptonow.com/pn/two-brothers-khapli-emmer-long-wheat-atta-stoneground/pvid/370fe3c6-58c9-42a1-af1f-8ce189a3efae',
        'https://www.zeptonow.com/pn/tata-sampann-unpolished-green-moong-dal/pvid/36153031-3e4e-4f9c-9082-16ec095479b4',
        'https://www.zeptonow.com/pn/anveshan-desi-buffalo-ghee/pvid/aaffddbe-d9c7-4dfa-bb0d-5ef88a6598d6',
        'https://www.zeptonow.com/pn/natureland-organics-ragi-flour/pvid/648580fb-c4df-4531-a966-3ef06a289d04',
        'https://www.zeptonow.com/pn/borges-extra-light-olive-oil/pvid/e143005a-dabf-4655-ace5-2977d241032a',
    ]
    i = 0
    for idx, url in enumerate(url_list[i:1], start=i):
        zepto = ZeptoData(url)
        zepto.extract_data()
        time.sleep(random.uniform(1.5, 3.5))

    # === Save to CSV ===
    df = pd.DataFrame(collect_product_data)
    file_name = 'zepto.csv'

    if os.path.exists(file_name):
        df.to_csv(file_name, mode='a', index=False, header=False)
        logger.info(f"Appended {len(df)} records to existing {file_name}")
    else:
        df.to_csv(file_name, mode='w', index=False)
        logger.info(f"Created {file_name} with {len(df)} records")

    logger.info("Scraping complete.")