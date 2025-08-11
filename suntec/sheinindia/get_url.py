import time
import random
from playwright.sync_api import sync_playwright

url = 'https://www.sheinindia.in/s/tshirts-133084'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    time.sleep(4)

    # Inject JavaScript to enable right-click
    page.evaluate("""
            document.addEventListener('contextmenu', event => event.stopPropagation(), true);
            document.oncontextmenu = null;
            document.body.oncontextmenu = null;
        """)

    print("Right-click has been enabled.")
    time.sleep(50)
    # for _ in range(50):
    #     page.evaluate("window.scrollBy(0, 100);")
    #     time.sleep(random.uniform(0.5, 0.15))
    #
    # page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(2)


    browser.close()
