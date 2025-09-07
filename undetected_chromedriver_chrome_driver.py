# from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as es
import time

# Use undetected Chrome driver
driver = uc.Chrome()
driver.maximize_window()

# List of URLs to scrape
url_list = ["https://www.mscdirect.com/product/details/04633335"]

for idx, url in enumerate(url_list, start=1):
    driver.get(url)
    time.sleep(15)

    try:
        # Wait until the part number is present
        wait = WebDriverWait(driver, 20)
        part_number_element = wait.until(es.presence_of_element_located((By.CSS_SELECTOR, "p#basePartNumber")))
        part_number = part_number_element.text.strip()
        print(f"[{idx}] Part Number: {part_number}")
    except Exception as e:
        print(f"[{idx}] Failed to retrieve part number for URL: {url}")
        print("Error:", e)



