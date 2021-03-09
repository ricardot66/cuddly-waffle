from bs4 import BeautifulSoup
from datetime import date
import requests
import math
import csv
import re

today = date.today()

sub_cats = [
    'https://listado.mercadolibre.com.mx/supermercado/comestibles-aceites-vinagres/',
    'https://listado.mercadolibre.com.mx/supermercado/comestibles-arroz-legumbres-semillas/',
    'https://listado.mercadolibre.com.mx/supermercado/comestibles-botanas/',
    'https://listado.mercadolibre.com.mx/supermercado/comestibles-cereales-barras/',
    'https://listado.mercadolibre.com.mx/supermercado/despensa-lupulo/',
    'https://listado.mercadolibre.com.mx/supermercado/despensa-pastas/',
    'https://listado.mercadolibre.com.mx/supermercado/comestibles-salsas-condimentos/',
    'https://listado.mercadolibre.com.mx/supermercado/despensa-algas-nori/',
    'https://listado.mercadolibre.com.mx/supermercado/comestibles-azucar-endulzantes/',
    'https://listado.mercadolibre.com.mx/supermercado/despensa-cafe-te-mate/',
    'https://listado.mercadolibre.com.mx/supermercado/despensa-dulces-chocolates/',
    'https://listado.mercadolibre.com.mx/supermercado/despensa-masa-empanadas/',
    'https://listado.mercadolibre.com.mx/supermercado/comestibles-pasteleria-reposteria/',
    'https://listado.mercadolibre.com.mx/supermercado/comestibles-alimentos-instantaneos/',
    'https://listado.mercadolibre.com.mx/supermercado/despensa-canastas-basicas/',
    'https://listado.mercadolibre.com.mx/supermercado/despensa-enlatados-conservas/',
    'https://listado.mercadolibre.com.mx/supermercado/despensa-mermeladas-miel/',
    'https://listado.mercadolibre.com.mx/supermercado/comestibles-saborizantes-jarabes/',
    'https://listado.mercadolibre.com.mx/supermercado/alimentos-bebidas/comestibles/otros/',

    'https://listado.mercadolibre.com.mx/supermercado/bebidas-sin-alcohol/aguas/',
    'https://listado.mercadolibre.com.mx/supermercado/bebidas-energeticas/',
    'https://listado.mercadolibre.com.mx/supermercado/bebidas-cervezas/',
    'https://listado.mercadolibre.com.mx/supermercado/bebidas-vinos-espumosos/',
    'https://listado.mercadolibre.com.mx/supermercado/bebidas-aperitivos/',
    'https://listado.mercadolibre.com.mx/supermercado/bebidas-isotonicas/',
    'https://listado.mercadolibre.com.mx/supermercado/bebidas-jugos/',
    'https://listado.mercadolibre.com.mx/supermercado/alimentos-bebidas/bebidas-sin-alcohol/otros/',
    'https://listado.mercadolibre.com.mx/supermercado/bebidas-blancas-licores/',
    'https://listado.mercadolibre.com.mx/supermercado/bebidas-preparadas/',
    'https://listado.mercadolibre.com.mx/supermercado/bebidas-sin-alcohol/refrescos/'
]

for sub_cat in sub_cats:
    with open('super.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(['snapshot_date', 'page', 'item_id', 'title', 'seller_id', 'category_id',
                             'official_store_id', 'price', 'base_price', 'original_price',
                             'initial_quantity', 'sold_quantity', 'listing_type_id', 'start_time',
                             'stop_time', 'permalink', 'shipping_free', 'shipping_logistic_type',
                             'seller_city', 'seller_state', 'seller_neighbourhood', 'deals_id'])
        web = requests.get(sub_cat)
        soup = BeautifulSoup(web.text, 'lxml')
        results = soup.find('span', class_='ui-search-search-result__quantity-results').text
        results = results.replace(' resultados', '')
        results = results.replace(',', '')
        pages = math.floor(int(results) / 50)

        for page in range(pages + 1):
            web = requests.get(sub_cat + '_Desde_' + str(48 * page + 1))
            soup = BeautifulSoup(web.text, 'lxml')

            for link in soup.find_all('a', class_='ui-search-result__content ui-search-link'):
                link = link['href']
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
                    try:
                        seller_neighbourhood = s['seller_address']['search_location']['neighborhood']['name']
                    except KeyError:
                        seller_neighbourhood = ""
                    deal_ids = s['deal_ids']

                    csv_writer.writerow(
                        [today.strftime("%d/%m/%Y"), int(page) + 1, item_id, title, seller_id, category_id,
                         official_store_id,
                         price, base_price, original_price, initial_quantity,
                         sold_quantity, listing_type_id, start_time, stop_time,
                         permalink, shipping_free, shipping_logistic_type,
                         seller_city, seller_state, seller_neighbourhood, deal_ids])

                except:
                    print('KEY ERROR')
                    continue
                print(page, r2, title)
