from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import requests
import constants
import json

class Ivivu:
    def __init__(self):
        _options = webdriver.ChromeOptions()
        _options.add_argument('--headless')
        _options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=_options)

        self.list_url_hotels = []
        self.list_hotels_data = []

    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
        content = requests.get(url, headers=headers).text

        return content

    def get_list_hotels(self):
        self.driver.get(constants.TARGET_URL)

        for hotel in self.driver.find_elements(By.CSS_SELECTOR, constants.HOTEL_ITEM):
            self.list_url_hotels.append(hotel.get_attribute('href'))

    def get_hotel_details(self):
        for list_item in self.list_url_hotels:
            html = self.get_html(list_item)

            soup = BeautifulSoup(html, 'lxml')

            hotel_name = soup.select_one(constants.HOTEL_NAME).text.replace('\xa0', ' ').splitlines()
            hotel_address = soup.select_one(constants.HOTEL_ADDRESS).text.replace('\xa0', ' ').splitlines()
            # hotel_price = soup.select_one(constants.HOTEL_PRICE).text
            hotel_description = soup.select_one(constants.HOTEL_DESCRIPTION).text.replace('\xa0', ' ').splitlines()

            print(f'Crawling hotel: {hotel_name} ...')

            # print(hotel_address)
            # print(hotel_description)

            faci_items = []
            for faci_item in soup.select(constants.HOTEL_FACI_ITEMS):
                faci_items.append(faci_item.text)

            self.list_hotels_data.append({
                'name': hotel_name,
                'address': hotel_address,
                'description': hotel_description,
                'faci_items': faci_items
            })
            break
    def get_csv_output(self):
        df = pd.DataFrame({'Name':self.list_hotels_data[i]['name'] for i in len(self.list_hotels_data)})
        df.to_csv('data.csv', encoding='utf-8')
    def get_json_output(self):
        print(self.list_hotels_data)
        with open('hotels.json', 'w', encoding='utf8') as f:
            json.dump(self.list_hotels_data, f, ensure_ascii = False)

        print('Done!!!')

def main():
    app = Ivivu()
    app.get_list_hotels()
    app.get_hotel_details()
    app.get_json_output()

if __name__ == '__main__':
    main()
