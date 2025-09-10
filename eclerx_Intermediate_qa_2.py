
"""
Task 2: Dynamic Page Scraping (Intermediate)
Website: https://quotes.toscrape.com/js/ (JavaScript-rendered version)
    Requirements:
Use Selenium or Playwright to extract the data (quotes, authors, tags).
Handle pagination until the "Next" button is no longer available.
Save output in JSON format.

"""
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def get_response_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def extraction():
    driver = get_response_selenium()
    all_quotes = []

    for i in range(1, 4):
        product_url = f'https://quotes.toscrape.com/js/page/{i}/'
        driver.get(product_url)
        time.sleep(2)

        quote_elements = driver.find_elements(By.CSS_SELECTOR, 'div.quote')
        for el in quote_elements:
            quote_text = el.find_element(By.CSS_SELECTOR, 'span.text').text.strip()
            author = el.find_element(By.CSS_SELECTOR, 'small.author').text.strip()
            tag_elements = el.find_elements(By.CSS_SELECTOR, 'div.tags a.tag')
            tags = [tag.text.strip() for tag in tag_elements]

            all_quotes.append({
                "quote": quote_text,
                "author": author,
                "tags": tags
            })

    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(all_quotes, f, ensure_ascii=False, indent=4)

    driver.quit()
    print("Data saved to quotes.json")

if __name__ == "__main__":
    extraction()
