import sqlite3
import requests
import json
from bs4 import BeautifulSoup

def get_augment_data(query, stage):
    stage_map = {'2-1': 'p1', '3-2': 'p2', '4-2': 'p3'}
    current_stage = stage_map[stage]
    url = 'https://tactics.tools/augments'
    response = requests.get(url)

    conn = sqlite3.connect('data/tft.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM augment WHERE name LIKE ?", ('%' + query + '%',))
    row = cur.fetchone()

    conn.close()

    query_id = row['tactics_id']
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
    
        json_string = script_tag.string if script_tag else ''

        # Parse the JSON string into a Python dictionary
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError:
            data = {}  # or handle the error as you see fit
        
        augment_list = data['props']['pageProps']['augsData']['singles']

        for augment in augment_list:
            if augment.get('id') == query_id:
                augment_info = augment[current_stage]
                augment_info['name'] = query
                return augment_info
    else:
        print("Failed to Scrape")

def get_highest(data_first, data_second, data_third, comparator):
    data_list = [data_first, data_second, data_third]

    highest_data = max(data_list, key=lambda x: x[comparator])

    return highest_data
    

