from selenium import webdriver
import undetected_chromedriver as e
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()

url_list = [
    "https://www.mscdirect.com/product/details/04633335"
]
for idx, url in enumerate(url_list[:], start=1):
    driver.get(url)
    time.sleep(10)

    part_number = driver.find_element(By.CSS_SELECTOR, 'div p[id="basePartNumber"]').text.strip()
    print(part_number)

driver.close()