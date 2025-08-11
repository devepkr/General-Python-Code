import asyncio
from playwright.async_api import async_playwright


async def get_cookies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://ar.shein.com/", wait_until="load")

        # Wait for session cookies to be set
        await asyncio.sleep(3)

        # Retrieve all cookies from the context (includes session cookies)
        cookies = await context.cookies()

        # Optional: Print or filter session cookies
        session_cookies = [cookie for cookie in cookies if not cookie.get("expires")]
        print("Session Cookies:", session_cookies)

        await browser.close()
        return cookies


# To run the async function
asyncio.run(get_cookies())
