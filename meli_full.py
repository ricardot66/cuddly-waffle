from scraper_api import ScraperAPIClient
from bs4 import BeautifulSoup
from datetime import date
import requests
import math
import csv
import re

today = date.today()

p_cat = []
client = ScraperAPIClient('Insert client here')

cats = ['MLM1367', 'MLM1368', 'MLM1384', 'MLM1246', 'MLM1039', 'MLM1051', 'MLM1648', 'MLM1144', 'MLM1276', 'MLM1575',
       'MLM1000', 'MLM186863', 'MLM1574', 'MLM1499', 'MLM1182', 'MLM3937', 'MLM1132', 'MLM3025', 'MLM1168', 'MLM1430',
       'MLM187772']

excluded = ["MLM1747", "MLM189530", "MLM1403", "MLM1071", "MLM1743", "MLM1459", "MLM44011", "MLM1540", "MLM1953"]

cat_counter = 0
for cat in cats:
    cat_api = requests.get('https://api.mercadolibre.com/categories/' + str(cat))
    s = cat_api.json()

    cat_name = s['name']
    permalink = s['permalink']

    web = requests.get(permalink)
    soup = BeautifulSoup(web.text, 'lxml')
    cat_soup = soup.find('div', class_='desktop__view-child')
    cat_counter += 1

    for a in cat_soup.find_all('a'):
        with open('category_items/FULL/' + str(cat_name).replace(' ', '_') + '_items_test_9.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(['snapshot_date', 'page', 'item_id', 'title', 'seller_id', 'category_id',
                                 'official_store_id', 'price', 'base_price', 'original_price',
                                 'initial_quantity', 'sold_quantity', 'listing_type_id', 'start_time',
                                 'stop_time', 'permalink', 'shipping_free', 'shipping_logistic_type',
                                 'seller_city', 'seller_state', 'seller_neighbourhood', 'deals_id'])

            cat_link = a['href']
            r1 = re.search(r"#CATEGORY_ID=MLM(\d+)[\s\S]+", cat_link).group(0)
            clean_link = cat_link.replace(r1, '')

            # paging goes in increments of 50
            full_web = client.get(clean_link + '_Envio_Full_Desde_01')
            # cat_web = client.get(clean_link) REGULAR LINK WITHOUT FILTERS
            full_soup = BeautifulSoup(full_web.text, 'lxml')
            try:
                full_results = full_soup.find('span', class_='ui-search-search-result__quantity-results').text
                full_results = full_results.replace(' resultados', '')
                full_results = full_results.replace(',', '')
                pages = math.floor(int(full_results)/50)
                if pages > 41:
                    pages = 41

            except AttributeError:
                print("pages not found")
                pages = 1

            print(str(r1) + ' scrape initiating...')

            for n in range(pages):
                n_web = client.get(clean_link + '_Envio_Full_Desde_' + str(50 * n + 1))
                soup = BeautifulSoup(n_web.text, 'lxml')

                for i in soup.find_all('div', class_='ui-search-item__group ui-search-item__group--title'):
                    try:
                        link = i.next['href']
                    except KeyError:
                        break
                    try:
                        r2 = re.search(r"MLM(-?)\d+", link).group(0)
                        r2 = r2.replace('-', '')
                    except AttributeError:
                        print('r2 error')
                        continue

                    item_web = requests.get('https://api.mercadolibre.com/items/' + r2)
                    print(item_web)
                    s = item_web.json()

                    try:
                        item_id = s['id']
                        title = s['title']
                        seller_id = s['seller_id']
                        category_id = s['category_id']
                        official_store_id = s['official_store_id']
                        price = s['price']
                        base_price = s['base_price']
                        original_price = s['original_price']
                        initial_quantity = s['initial_quantity']
                        sold_quantity = s['sold_quantity']
                        listing_type_id = s['listing_type_id']
                        start_time = s['start_time']
                        stop_time = s['stop_time']
                        permalink = s['permalink']
                        shipping_free = s['shipping']['free_shipping']
                        shipping_logistic_type = s['shipping']['logistic_type']
                        seller_city = s['seller_address']['city']['name']
                        seller_state = s['seller_address']['state']['name']
                        seller_neighbourhood = s['seller_address']['search_location']['neighborhood']['name']
                        deal_ids = s['deal_ids']

                        csv_writer.writerow([today.strftime("%d/%m/%Y"), int(n) + 1, item_id, title, seller_id, category_id, official_store_id,
                                             price, base_price, original_price, initial_quantity,
                                             sold_quantity, listing_type_id, start_time, stop_time,
                                             permalink, shipping_free, shipping_logistic_type,
                                             seller_city, seller_state, seller_neighbourhood, deal_ids])

                    except KeyError:
                        continue
                    print(cat_counter, n, r2, title)
