from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
import matplotlib.pyplot as plt
import time
import logging
from screeninfo import get_monitors
from selenium.webdriver.chrome.options import Options




# Logging configuration
# === Logging configuration to file AND terminal ===
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler('run.log', mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logging.info("=" * 80)
logging.info("Script started.")

monitor = get_monitors()[0]
width, height = monitor.width, monitor.height
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument(f"window-size={width},{height}")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()


scroll_down = "window.scrollBy(0, 500);"


class BarChart:
    def __init__(self, URL, DRIVER):
        self.url = URL
        self.driver = DRIVER

    def click_to_pop_up_close_button(self):
        try:
            popup_button_1_xpath = '(//i[@data-ng-click="close();"])[2]'
            popup_button_1 = self.driver.find_element(By.XPATH, popup_button_1_xpath)
            if popup_button_1.is_displayed():
                popup_button_1.click()
                logging.info('Clicked first pop-up close button.')
                time.sleep(0.5)
            else:
                logging.info('First pop-up button found but not visible.')
        except NoSuchElementException:
            logging.info('First pop-up button not found...')
        except ElementNotInteractableException:
            logging.info('First pop-up button is not interactable...')

        try:
            popup_button_xpath = '//span[@class="adthrive-close"]'
            popup_button = self.driver.find_element(By.XPATH, popup_button_xpath)
            popup_button.click()
            logging.info('Clicked second pop-up close button.')
            time.sleep(0.5)
            self.driver.execute_script(scroll_down)
            time.sleep(0.5)
        except NoSuchElementException:
            logging.info(f'Second pop-up button not found...')

    def get_data(self):
        self.click_to_pop_up_close_button()

        table_locator = '//*[@id="main-content-column"]/div/div[3]/div[2]'
        table = self.driver.find_element(By.XPATH, table_locator).text.strip()
        table_data = table.strip().split('\n')
        headers = table_data[2:9]
        data_rows = []
        for i in range(10, len(table_data), 7):
            if i + 7 <= len(table_data):
                table_row = table_data[i:i + 7]
                data_rows.append(table_row)
        df = pd.DataFrame(data_rows, columns=headers)
        # print(df.to_string())

        # a)Create a new column named “Mean” that which will be the mean of column “High” and “Low”.
        df["Low"] = df["Low"].replace(",", "", regex=True).replace("-", ".", regex=True).astype(float)
        df["High"] = df["High"].replace(",", "", regex=True).replace("-", ".", regex=True).astype(float)
        df['Mean'] = (df['High'] + df['Low']) / 2
        logging.info("Extracted and cleaned data:\n" + df.to_string())

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
        max_changes = df['Change'].idxmax() # max
        logging.info(f"\nContract with largest change: {df.loc[max_changes, 'Contract Name']}")
        logging.info(f"Last price: {df.loc[max_changes, 'Last']}")
        logging.info(f"Largest change: {df.loc[max_changes, 'Change']}%")

        #---------------------------------------------------------------------------------------------------------------
        min_changes = df['Change'].idxmin()  # min
        logging.info(f"\nContract with smallest change: {df.loc[min_changes, 'Contract Name']}")
        logging.info(f"Last price: {df.loc[min_changes, 'Last']}")
        logging.info(f"Smallest change: {df.loc[min_changes, 'Change']}%")


        # d) The extracted data needs to be saved with the sheet name as “Raw Data” in an Excel workbook.
        save_file_path = r"P:\Python_code\Matplotlib\files\futures_data.xlsx"
        df.to_excel(save_file_path, sheet_name="Raw Data", index=False)
        print("Data saved to 'futures_data.xlsx' under sheet 'Raw Data'")
        logging.info(f"Data saved to Excel at: {save_file_path}")


if __name__ == "__main__":
    try:
        url = 'https://www.barchart.com/futures'
        driver.get(url)
        time.sleep(5)
        barchart_objects = BarChart(url, driver)
        barchart_objects.get_data()
        logging.info("Script completed successfully.")
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}")
    finally:
        driver.quit()
        logging.info("Driver closed.")
        logging.info("Script ended.")
        logging.info("=" * 80)