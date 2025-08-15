import json
import requests
import pandas as pd
from urllib.parse import unquote
import matplotlib.pyplot as plt

# Initialize session
session = requests.Session()

def hit_home_page():
    headers_ = {
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
    print(initial_url)
    response_ = session.get(initial_url, headers=headers_)
    print(response_.status_code)

    # Extract cookies
    cookies = session.cookies.get_dict()
    laravel_token_1 = cookies.get('laravel_token')
    xsrf_token_1 = cookies.get('XSRF-TOKEN')
    if not laravel_token_1 or not xsrf_token_1:
        raise ValueError("Failed to retrieve laravel_token or XSRF-TOKEN from cookies")

    xsrf_token_2 = unquote(xsrf_token_1)
    # print('xsrf_token_2 >>>>', xsrf_token_2)
    return xsrf_token_2, laravel_token_1

def api_headers(xsrf_token_2):
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
        'x-xsrf-token': xsrf_token_2,
    }

def hit_apis(URL, api_headers_, laravel_token_1):
    response = session.get(URL, cookies={'laravel_token': laravel_token_1}, headers=api_headers_)
    if response.status_code == 200:
        json_data = json.loads(response.content)
        data = json_data['data']

        market_data = []
        for item in data:
            market_data.append({
                'Contract Name': item['contractName'],
                'Last': item['lastPrice'],
                'Change': item['priceChange'],
                'High': item['highPrice'],
                'Low': item['lowPrice'],
                'Volume': item['volume'],
                'Time': item['tradeTime'],
            })

        df = pd.DataFrame(market_data)
        # a)Create a new column named “Mean” that which will be the mean of column “High” and “Low”.
        df["Low"] = df["Low"].replace(",", "", regex=True).replace("-", ".", regex=True).astype(float)
        df["High"] = df["High"].replace(",", "", regex=True).replace("-", ".", regex=True).astype(float)
        df['Mean'] = (df['High'] + df['Low']) / 2
        print(df.to_string())

        # b) Plot “High”, “Low” and “Mean” in a single linear graph.
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['High'], label='High', marker='o')
        plt.plot(df.index, df['Low'], label='Low', marker='o')
        plt.plot(df.index, df['Mean'], label='Mean', marker='o')
        # Customize the plot
        plt.xlabel('Contract Index')
        plt.ylabel('Price')
        plt.title('High, Low, and Mean Prices of Futures Contracts')
        plt.legend()
        plt.grid(True)
        # Set x-ticks to show contract names (rotated for readability)
        plt.xticks(df.index, df['Contract Name'], rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        # c) Find the “Contract Name” and “Last” of the row that has largest “Change”
        df['Change'] = pd.to_numeric(df['Change'].str.replace('%', ''), errors='coerce')
        max_changes = df['Change'].idxmax()  # max
        print(f"\nContract with largest change: {df.loc[max_changes, 'Contract Name']}")
        print(f"Last price: {df.loc[max_changes, 'Last']}")
        print(f"Largest change: {df.loc[max_changes, 'Change']}%")

        # ---------------------------------------------------------------------------------------------------------------
        min_changes = df['Change'].idxmin()  # min
        print(f"\nContract with smallest change: {df.loc[min_changes, 'Contract Name']}")
        print(f"Last price: {df.loc[min_changes, 'Last']}")
        print(f"smallest change: {df.loc[min_changes, 'Change']}%")

        # d) The extracted data needs to be saved with the sheet name as “Raw Data” in an Excel workbook.
        save_file_path = r"P:\Python_code\Matplotlib\files\futures_data.xlsx"
        df.to_excel(save_file_path, sheet_name="Raw Data", index=False)
        print("Data saved to 'futures_data.xlsx' under sheet 'Raw Data'")


    else:
        print(f"API request failed with status code: {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    xsrf_token, laravel_token = hit_home_page()
    url = 'https://www.barchart.com/proxies/core-api/v1/quotes/get?symbols=ES*0%2CNQ*0%2CYM*0%2CVI*0%2CDX*0%2CZN*0%2CCL*0%2CNG*0%2CGC*0%2CSI*0%2CZC*0%2CZW*0%2CZS*0%2CSB*0%2CKC*0%2CCC*0&fields=symbol%2CsymbolType%2CcontractName%2ClastPrice%2CpriceChange%2ChighPrice%2ClowPrice%2Cvolume%2CtradeTime%2ChasOptions%2CsymbolCode&meta=field.shortName%2Cfield.type%2Cfield.description&page=1&raw=1'
    headers = api_headers(xsrf_token)
    hit_apis(url, headers, laravel_token)