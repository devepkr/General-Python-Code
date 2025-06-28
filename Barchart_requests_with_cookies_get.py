import json
import requests
import pandas as pd
from urllib.parse import unquote

# Initialize session
session = requests.Session()

def hit_home_page():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

    initial_url = 'https://www.barchart.com/futures'
    response = session.get(initial_url, headers=headers)

    # Extract cookies
    cookies = session.cookies.get_dict()
    laravel_token = cookies.get('laravel_token')
    xsrf_token = cookies.get('XSRF-TOKEN')
    if not laravel_token or not xsrf_token:
        raise ValueError("Failed to retrieve laravel_token or XSRF-TOKEN from cookies")

    xsrf_token = unquote(xsrf_token)
    return xsrf_token, laravel_token

def api_headers(xsrf_token):
    return {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=1, i',
        'referer': 'https://www.barchart.com/futures',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'x-xsrf-token': xsrf_token,
    }

def hit_apis(url, api_headers, laravel_token):
    response = session.get(url, cookies={'laravel_token': laravel_token}, headers=api_headers)

    # Process the response
    if response.status_code == 200:
        json_data = json.loads(response.content)
        data = json_data['data']

        market_data = []
        for item in data:
            market_data.append({
                'Contract_Name': item['contractName'],
                'Last': item['lastPrice'],
                'Change': item['priceChange'],
                'High': item['highPrice'],
                'Low': item['lowPrice'],
                'Volume': item['volume'],
                'Time': item['tradeTime'],
            })

        df = pd.DataFrame(market_data)
        print(df.to_string())
    else:
        print(f"API request failed with status code: {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    xsrf_token, laravel_token = hit_home_page()
    url = 'https://www.barchart.com/proxies/core-api/v1/quotes/get?symbols=ES*0%2CNQ*0%2CYM*0%2CVI*0%2CDX*0%2CZN*0%2CCL*0%2CNG*0%2CGC*0%2CSI*0%2CZC*0%2CZW*0%2CZS*0%2CSB*0%2CKC*0%2CCC*0&fields=symbol%2CsymbolType%2CcontractName%2ClastPrice%2CpriceChange%2ChighPrice%2ClowPrice%2Cvolume%2CtradeTime%2ChasOptions%2CsymbolCode&meta=field.shortName%2Cfield.type%2Cfield.description&page=1&raw=1'
    headers = api_headers(xsrf_token)
    hit_apis(url, headers, laravel_token)