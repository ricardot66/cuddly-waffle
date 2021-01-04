from scraper_api import ScraperAPIClient
from bs4 import BeautifulSoup
from random import randint
from datetime import date
import requests
import csv
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

today = date.today()
client = ScraperAPIClient('5bccdaccabd41d848741374da5c0117c')
store_urls = []
seller_ids = []

with open('official_stores/official_store_' + today.strftime("%d%m%Y") + '.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['store_name', 'seller_id', 'nickname', 'registration_date', 'country_id',
                         'city', 'state', 'user_type', 'tags', 'points', 'permalink', 'level_id',
                         'power_seller_status', 'completed_transactions', 'canceled_transactions',
                         'total_transactions'])

# Get official stores urls
    web = requests.get("https://www.mercadolibre.com.mx/tiendas-oficiales/catalogo", headers=headers)
    soup = BeautifulSoup(web.text, 'lxml')

    for i in soup.find("div", class_="item-grid-show"):
        for h in i.find_all("a"):
            print(h['href'])
            store_urls.append(h['href'])

    # Loop through stores

    for url in store_urls:
        if randint(1, 10) % 3 == 0:
            url_soup = BeautifulSoup(requests.get(url).text, 'lxml')
            print("LOCAL REQUEST")
        else:
            url_soup = BeautifulSoup(client.get(url).text, 'lxml')
            print("PROXY REQUEST")

        try:
            store_name = url_soup.find("h1", "ui-search-breadcrumb__title").text
            item_link = url_soup.find("a", class_="ui-search-result__content ui-search-link")["href"]
            item_soup = BeautifulSoup(requests.get(item_link).text, 'lxml')
            print(str(store_name) + " open.")
            pattern = re.compile(r'"seller_id":\d+', re.MULTILINE | re.DOTALL)
            scripts = item_soup.find_all("script")
        except:
            continue

        for i in scripts:
            try:
                i_contents = i.string
                seller_id = re.search(r'"seller_id":\d+', i_contents).group(0)
                seller_id = seller_id.replace('"seller_id":', '')
                if seller_id in seller_ids:
                    continue
                else:
                    seller_ids.append(seller_id)

            except:
                continue

        for sid in seller_ids:
                try:
                    web = requests.get("https://api.mercadolibre.com/users/" + sid)
                    r = web.json()

                    nickname = r['nickname']
                    registration_date = r['registration_date']
                    country_id = r['country_id']
                    city = r['address']['city']
                    state = r['address']['state']
                    user_type = r['user_type']
                    tags = r['tags']
                    points = r['points']
                    permalink = r['permalink']
                    level_id = r['seller_reputation']['level_id']
                    power_seller_status = r['seller_reputation']['power_seller_status']
                    completed_transactions = r['seller_reputation']['transactions']['completed']
                    canceled_transactions = r['seller_reputation']['transactions']['canceled']
                    total_transactions = r['seller_reputation']['transactions']['total']

                    csv_writer.writerow([store_name, sid, nickname, registration_date,
                                         country_id, city, state, user_type, tags, points,
                                         permalink, level_id, power_seller_status, completed_transactions,
                                         canceled_transactions, total_transactions])
                    print("Real Seller: " + str(nickname) + seller_ids.pop(0))


                except:
                    print("PROXY REQUEST:")
                    try:
                        web = client.get("https://api.mercadolibre.com/users/" + sid)
                        r = web.json()

                        nickname = r['nickname']
                        registration_date = r['registration_date']
                        country_id = r['country_id']
                        city = r['address']['city']
                        state = r['address']['state']
                        user_type = r['user_type']
                        tags = r['tags']
                        points = r['points']
                        permalink = r['permalink']
                        level_id = r['seller_reputation']['level_id']
                        power_seller_status = r['seller_reputation']['power_seller_status']
                        completed_transactions = r['seller_reputation']['transactions']['completed']
                        canceled_transactions = r['seller_reputation']['transactions']['canceled']
                        total_transactions = r['seller_reputation']['transactions']['completed']

                        csv_writer.writerow([store_name, sid, nickname, registration_date,
                                             country_id, city, state, user_type, tags, points,
                                             permalink, level_id, power_seller_status, completed_transactions,
                                             canceled_transactions, total_transactions])
                        print("Real Seller: " + str(nickname))

                    except:
                        continue
