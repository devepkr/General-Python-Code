import requests
import random
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import  os

class SheinIndia:
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
        self.headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'priority': 'u=0, i',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    **random.choice(self.user_agent_list),
}

    def extract_data(self):
        name = []
        value = []
        variants_data = []
        specs_value = []

        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            script_tags = soup.find_all('script')
            script_content = None
            for script in script_tags:
                if script.string and 'window.__PRELOADED_STATE__' in script.string:
                    script_content = script.string
                    break
            if script_content:
                match = re.search(r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?});', script_content, re.DOTALL)
                if match:
                    json_text = match.group(1)
                    data = json.loads(json_text)
                    json_datas = data['product']
                    baseOptions = json_datas['productDetails']['featureData']
                    for specs_list in baseOptions:
                        name.append(specs_list['name'])
                        value.append(specs_list['featureValues'][0]['value'])
                    specs_value = [{v: n} for v, n in zip(name, value)]
                else:
                    print("Feature JSON data not found in the script.")
            else:
                print("Script with product data not found.")

            # Extract variant data
            scripts = soup.find_all('script', type='application/ld+json')
            if scripts:
                json_data = scripts[-1].string
                data = json.loads(json_data)
                json_item = data['hasVariant']
                for item in json_item:
                    variant = {
                        'url' : self.url,
                        'name': item.get('name', ''),
                        'size': item.get('size', ''),
                        'price': item.get('offers', {}).get('price', ''),
                        'sku': str(item.get('sku', '')),
                        'image': item.get('image', ''),
                        'specs': specs_value
                    }
                    variants_data.append(variant)

                variants_df = pd.DataFrame(variants_data)
                file_exists = os.path.isfile('variants.csv')
                variants_df.to_csv('variants.csv', mode='a+', header=not file_exists, index=False)
                print(variants_df.to_string())
            else:
                print("Variant JSON data not found.")
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")


if __name__ == "__main__":
    file_path = 'Book1.csv'
    read_files = pd.read_csv(file_path)['URL']
    cnt = 0
    for idx, url in enumerate(read_files[cnt:10], start=cnt):
        scraper = SheinIndia(url)
        scraper.extract_data()

