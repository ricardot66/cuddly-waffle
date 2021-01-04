from datetime import date, timedelta
import pandas as pd
import numpy as np
import requests
import csv
import os

os.remove(r'category_shapes/cat_desc_2.csv')
os.rename(r'category_shapes/cat_desc_1.csv', r'category_shapes/cat_desc_2.csv')

# Shape extraction
today = date.today()
last_week = today - timedelta(days=7)
with open('category_shapes/cat_desc_1.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['id', 'cat_name', 'sub_cat_name', 'num_items'])
    web = requests.get('https://api.mercadolibre.com/sites/MLM/categories')
    r = web.json()

    for cat in r:
        cat_api = requests.get('https://api.mercadolibre.com/categories/' + str(cat['id']))
        s = cat_api.json()

        cat_id = s['id']
        cat_name = s['name']
        cat_total_items = s['total_items_in_this_category']
        csv_writer.writerow([cat_id, cat_name, 'total', cat_total_items])
        for sub_cat in s['children_categories']:
            sub_cat_name = sub_cat['name']
            sub_cat_id = sub_cat['id']
            sub_cat_items = sub_cat['total_items_in_this_category']
            csv_writer.writerow([sub_cat_id, cat_name, sub_cat_name, sub_cat_items])

# Dataframe analysis
# df1 is new df, df2 the last one
df1 = pd.read_csv('category_shapes/cat_desc_1.csv')
df2 = pd.read_csv('category_shapes/cat_desc_2.csv')

# % changes
df1['last_week_items'] = df2['num_items']
df1['item_difference'] = np.where(df1['num_items'] == df2['num_items'], 0, df2['num_items'] - df1['num_items']) * -1
df1['percent_difference'] = df1['item_difference'] / df1['num_items']

df1.to_csv('category_shapes/Historical/cat_desc_' + today.strftime("%d%m%Y") + '.csv', index=False)

# Totals df
totals_df1 = df1[df1['sub_cat_name'] == 'total']
totals_df2 = df2[df2['sub_cat_name'] == 'total']

total_diff = totals_df1.num_items.sum() - totals_df2.num_items.sum()
total_pct_diff = 1 - totals_df1.num_items.sum() / totals_df2.num_items.sum()

totals_df1.to_excel('category_shapes/Analysis/analysis_' + today.strftime("%d%m%Y") + '.xlsx', sheet_name='week_totals',
                    index=False)
