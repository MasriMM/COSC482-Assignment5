#importing needed libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#setup and configuration
options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

#function to scroll at the end of the page
def infinite_scroll():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  
        last_height = new_height

URL = "https://www.ebay.com/globaldeals/tech"

#function to scrape the data
def scrape_ebay_data():
    driver.get(URL)
    time.sleep(10)

    infinite_scroll()

    all_products = []
    try: 
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".dne-itemtile")))

        for product in products:
            try:
                tile = product.find_element(By.XPATH, ".//span[contains(@itemprop,'name')]").text
            except:
                tile ="N/A"
            try:
                price = product.find_element(By.XPATH, ".//span[contains(@itemprop,'price')]").text
            except:
                price="N/A"
            try:
                original_price = product.find_element(By.XPATH, ".//span[contains(@class,'itemtile-price-strikethrough')]").text
            except:
                original_price="N/A"
            try:
                shipping = product.find_element(By.XPATH, ".//span[contains(@class,'dne-itemtile-delivery')]").text
            except:
                shipping="N/A"
            try:
                item_url = product.find_element(By.XPATH, ".//a[contains(@itemprop,'url')]").get_attribute("href")
            except:
                item_url = "N/A"
        
            products_data = {
                "timestamp": timestamp,
                "tile": tile,
                "price": price,
                "original_price": original_price,
                "shipping": shipping,
                "item_url": item_url
            }
            all_products.append(products_data)

        return all_products
    except Exception as e:
        print("Error occurred:", e)

#function to save the scraped data into .csv file
def save_to_csv(data):
    file_name = "ebay_tech_deals.csv"
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["timestamp", "tile", "price", "original_price", "shipping", "item_url"])

    new_row = pd.DataFrame(data)

    df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(file_name, index=False)

#main to call functions
if __name__ == "__main__":
    print("Scraping Ebay Data...")
    scraped_data = scrape_ebay_data()

    if scraped_data:
        save_to_csv(scraped_data)
        print("Data saved to ebay_tech_deals.csv")
    else:
        print("Failed to scrape data")
    
    driver.quit()