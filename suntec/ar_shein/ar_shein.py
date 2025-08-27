import time
import random
import  pandas as pd
import asyncio
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
session = requests.Session()

async def get_cookies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://ar.shein.com/", wait_until="load")
        # await page.goto(url, wait_until="load")
        await asyncio.sleep(1)
        cookies = await context.cookies()
        return cookies


user_agent_list = [
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
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'priority': 'u=0, i',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    **random.choice(user_agent_list),
}


def make_requests(URL):
    co_list = asyncio.run(get_cookies())  # list of cookies
    for idx, cookie in enumerate(co_list):
        try:
            single_cookie = {cookie['name']: cookie['value']}
            # single_cookie = {'_f_c_llbs_':'K1905_1753673113_QrOTcD3I6-4LpTc7xz_jdb_2-cONkZ9gwf2wIBN2xJ9iMRWPS9BW6FjWF_Lt3I4VouE3qYogCI18nRApQOpeAhZ2fEmxHa2-ImAobn9D9-j6vhLj0V40zzN6N5ZBbz3iLUb8fQuxHn1_S04cfqWap7K3StgvrUGMoDD1StdzgaugENAQEsWwLQNRFOskcDUUoumdxMX7GUAu4UwLw8ROZUrvpCTrPCbEZFEkEZ2RtcPBVvH-eNJZDNv4r8NoTNCv-TwlSLdvNfqqMCPVmWK2P_EZHuNj--vwv31jzTTebV9UGGBi4h-iGEoyvpn9BjZ1A0a5JQVbzI5X1ZcDyoAPJw'}
            print(f'Trying cookie {idx + 1}:', single_cookie)
            ress = session.get(URL, headers=headers, cookies=single_cookie, timeout=10)
            if ress.status_code == 200 and 'productMainPriceId' in ress.text:
                soup = BeautifulSoup(ress.content, 'lxml')
                print('Success with cookie:', single_cookie)
                return soup
            else:
                print(f"Cookie {idx + 1} failed (Status: {ress.status_code})")
        except Exception as e:
            print(f"Error with cookie {idx + 1}: {e}")
    print(f"Failed to fetch {URL} with all cookies.")
    return None

all_data = []
def extract_data(soup):
    print('url---:', url)
    title = soup.select_one('h1[class="title-line-camp product-intro__head-name"]').text.strip()
    breadcrumb = [item.text.strip().replace('/', '>>>') for item in soup.select('.bread-crumb__inner .bread-crumb__item')]
    sku_number = soup.select_one('div[class="product-intro__head-sku"]').text.strip()
    price_ = soup.select_one('div[id="productMainPriceId"]').text.strip()

    print(f"Breadcrumb: {breadcrumb}")
    # print(f"Title: {title}")
    print(f"SKU Number: {sku_number}")
    print(f"Price: {price_}")

    all_data.append({
        'URL': url,
        'Title': title,
        'Breadcrumb': ' > '.join(breadcrumb),
        'SKU Number': sku_number,
        'Price': price_
    })


def run_scraper(URL):
    soup  = make_requests(URL)
    extract_data(soup)


if __name__ == "__main__":
    file_path = "product_urls.csv"
    read_file = pd.read_csv(file_path)['URL']

    i = 0
    for idx, url in enumerate(read_file[i:1], start=i):
        run_scraper(url)
        time.sleep(1)

    df = pd.DataFrame(all_data)
    df.to_csv(r"extracted_product_data.csv", index=False)
    print("Data saved to extracted_product_data.csv")