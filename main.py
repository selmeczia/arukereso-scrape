# This is a sample Python script.
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import os
import config as cfg


def scrape_products():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Scraping items from products.csv at " + current_time)
    print("Next run will be approximately " + str(cfg.minutes) + " minutes from now")
    products = pd.read_csv(cfg.products_path)

    for index, row in products.iterrows():
        name = row.tolist()[0] + ".csv"
        link = row.tolist()[1]

        path = "./output/ " + name

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

            price_list.append(int(item_price))
            store_list.append(store_name)
            link_list.append(item_link)

        if not (price_list):
            pass
        else:
            min_price = min(price_list)
            df = pd.DataFrame(list(zip(price_list, store_list, link_list)), columns=['Price', "Store", "Link"])
            df["Min price"] = min_price
            df["Date"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            df = df[["Date", "Price", "Min price", "Store", "Link"]]

            df['Latest_run'] = ""

            # if not first run:
            if os.path.isfile(path):
                df['Latest_run'] = 1
                imported = pd.read_csv(path)
                imported_without_latest = imported[imported['Latest_run'] == 0]
                imported_only_latest = imported[imported['Latest_run'] == 1].copy()
                # https://www.dataquest.io/blog/settingwithcopywarning/
                imported_only_latest['Latest_run'] = 0
                latest_and_current = imported_only_latest.append(df)
                removed_duplicates = latest_and_current.drop_duplicates(subset=['Store', 'Price'], keep='last')

                output = imported_without_latest.append(removed_duplicates)
                df = output

            else:
                df['Latest_run'] = 0

            # latest_run_df = imported[imported.Latest_run == 1]

                # delete the same rows from imported as the newly added
                # i = 0
                # for store in imported.Store.unique():
                #     imported_value = imported.loc[imported['Store'] == store, 'Price'].tolist()[0]
                #     existing_value = df.loc[df['Store'] == store, 'Price'].tolist()[0]
                #     if (imported_value == existing_value):
                #         imported = imported.loc[imported['Store'] != store]
                #     i =+ 1
                # #    if imported.loc[imported['Latest_run'] == 1, 'Price'] == df.loc[['Price']]:
                # #        print("helo")
                #
                # df[['Latest_run']] = 1

                # existing_min_price = imported.iloc[-1, 2]
                # if (int(min_price) < int(existing_min_price)):
                #     row = df.loc[df['Price'] == min_price]
                #     message = "The lowest price has changed! It is now: " + str(min_price) + " Ft instead of " + str(existing_min_price) + " Ft on the site: " + row.iloc[0,3]
                #     message2 = "Check the link: " + row.iloc[0, 4]
                #     print(message + "\n" + message2)
                # elif (int(min_price) > int(existing_min_price)):
                #     row = df.loc[df['Price'] == min_price]
                #     message = "Oh no! The lowest price has changed to " + str(min_price) + " Ft inestead of " + str(existing_min_price) + " Ft"

            # df = df.drop_duplicates(subset=['Store', 'Price'], keep='last')

            df.to_csv(path, index=False, header=True)
