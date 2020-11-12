# This is a sample Python script.
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import os
import time
#from apscheduler.scheduler import Scheduler

products = pd.read_csv("products.csv")

def scrape_products():

    for index, row in products.iterrows():
        name = row.tolist()[0] + ".csv"
        link = row.tolist()[1]

    #link = "https://www.arukereso.hu/jatekkonzol-c3154/sony/playstation-5-ps5-p588030129/"
    #csv_name = "arukereso_PS5.csv"

        path = "./output/" + name

        source = requests.get(link).text
        soup = BeautifulSoup(source, 'lxml')

        price_list = []
        store_list = []
        link_list = []

        for item in soup.find_all('div', class_='optoffer device-desktop'):

            item_price_raw = item.find('div', class_='row-price').text
            item_price = item_price_raw.split(' Ft')[0].replace(' ', '')

            store_name = item.find('div', class_='shopname').text

            link = item.find('a', class_='jumplink-overlay initial')
            item_link = link['href']

            price_list.append(item_price)
            store_list.append(store_name)
            link_list.append(item_link)

        min_price = min(price_list)
        df = pd.DataFrame(list(zip(price_list, store_list, link_list)), columns=['Price',"Store", "Link"])
        df["Min price"] = min_price
        df["Date"] = datetime.now().strftime("%d/%m/%Y %H:%M")


        df = df[["Date", "Price", "Min price", "Store", "Link"]]


        if (os.path.isfile(path)):

            imported = pd.read_csv(path)

            # existing_min_price = imported.iloc[-1, 2]
            # if (int(min_price) < int(existing_min_price)):
            #     row = df.loc[df['Price'] == min_price]
            #     message = "The lowest price has changed! It is now: " + str(min_price) + " Ft instead of " + str(existing_min_price) + " Ft on the site: " + row.iloc[0,3]
            #     message2 = "Check the link: " + row.iloc[0, 4]
            #     print(message + "\n" + message2)
            # elif (int(min_price) > int(existing_min_price)):
            #     row = df.loc[df['Price'] == min_price]
            #     message = "Oh no! The lowest price has changed to " + str(min_price) + " Ft inestead of " + str(existing_min_price) + " Ft"

            df = imported.append(df)

        df.to_csv(path, index = False, header= True)

