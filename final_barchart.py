from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import matplotlib.pyplot as plt
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

click_to_popup_button = 'div[id="onetrust-close-btn-container"] [aria-label="Close"]'
scroll_down = "window.scrollBy(0, 300);"
table_locator = '//*[@id="main-content-column"]/div/div[3]/div[2]'


class BarChart:
    def __init__(self, URL, DRIVER):
        self.url = URL
        self.driver = DRIVER

    def get_data(self):
        try:
            popup_button = self.driver.find_element(By.CSS_SELECTOR, click_to_popup_button)
            popup_button.click()
            time.sleep(0.5)
            self.driver.execute_script(scroll_down)
            time.sleep(0.7)
        except Exception as e:
            print(f'Pop up button not found: {str(e)}')

        table = self.driver.find_element(By.XPATH, table_locator).text.strip()
        table_data = table.strip().split('\n')
        headers = table_data[2:9]
        print(headers)
        data_rows = []
        for i in range(9, len(table_data), 7):
            # Ensure we have a complete set of 7 elements
            if i + 7 <= len(table_data):
                table_row = table_data[i:i+7]
                # Append an empty string for the 'Links' column
                data_rows.append(table_row + [''])
        df = pd.DataFrame(data_rows, columns=headers)
        print(df.to_string())

        # # a)Create a new column named “Mean” that which will be the mean of column “High” and “Low”.
        # df["Low"] = df["Low"].replace(",", "", regex=True).replace("-", ".", regex=True).astype(float)
        # df["High"] = df["High"].replace(",", "", regex=True).replace("-", ".", regex=True).astype(float)
        # df['Mean'] = (df['High'] + df['Low']) / 2
        # print(df.to_string())
        #
        # # b) Plot “High”, “Low” and “Mean” in a single linear graph.
        # plt.figure(figsize=(12, 6))
        # plt.plot(df.index, df['High'], label='High', marker='o')
        # plt.plot(df.index, df['Low'], label='Low', marker='o')
        # plt.plot(df.index, df['Mean'], label='Mean', marker='o')
        # # Customize the plot
        # plt.xlabel('Contract Index')
        # plt.ylabel('Price')
        # plt.title('High, Low, and Mean Prices of Futures Contracts')
        # plt.legend()
        # plt.grid(True)
        # # Set x-ticks to show contract names (rotated for readability)
        # plt.xticks(df.index, df['Contract Name'], rotation=45, ha='right')
        # plt.tight_layout()
        # plt.show()
        #
        #
        # # c) Find the “Contract Name” and “Last” of the row that has largest “Change”
        # df['Change'] = pd.to_numeric(df['Change'].str.replace('%', ''), errors='coerce')
        # max_changes = df['Change'].idxmax() # max
        # print(f"\nContract with largest change: {df.loc[max_changes, 'Contract Name']}")
        # print(f"Last price: {df.loc[max_changes, 'Last']}")
        # print(f"Largest change: {df.loc[max_changes, 'Change']}%")
        #
        # #---------------------------------------------------------------------------------------------------------------
        # min_changes = df['Change'].idxmin()  # min
        # print(f"\nContract with smallest change: {df.loc[min_changes, 'Contract Name']}")
        # print(f"Last price: {df.loc[min_changes, 'Last']}")
        # print(f"smallest change: {df.loc[min_changes, 'Change']}%")
        #
        #
        # # d) The extracted data needs to be saved with the sheet name as “Raw Data” in an Excel workbook.
        # save_file_path = r"P:\Python_code\Matplotlib\files\futures_data.xlsx"
        # df.to_excel(save_file_path, sheet_name="Raw Data", index=False)
        # print("Data saved to 'futures_data.xlsx' under sheet 'Raw Data'")


if __name__ == "__main__":
    url = 'https://www.barchart.com/futures'
    driver.get(url)
    time.sleep(5)
    barchart_objects = BarChart(url, driver)
    barchart_objects.get_data()
    driver.quit()