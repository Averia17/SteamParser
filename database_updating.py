import re
from concurrent.futures import ThreadPoolExecutor

import requests

from bitskins import updatedBitskinsItems
from models import conn, cur

steam_names = []
list_to_insert = []


def adding_to_db():
    cur.execute(
        "SELECT name, steamlink, steamid, price FROM steaminfo ")  # WHERE price::decimal > 0.1 AND NAME NOT LIKE '★%'
    rows = cur.fetchall()
    for row in rows:
        steam_names.append(row[0])
    # if you have not rows in database comment this assert
    assert len(steam_names) != 0, 'List steam names null'

    with ThreadPoolExecutor(max_workers=10) as executor:
        for item in updatedBitskinsItems:
            executor.map(getItemsToInsert, [item])
        executor.shutdown(wait=True)
    insertToDatabase()


def getItemsToInsert(item):
    steam_link = 'https://steamcommunity.com/market/listings/730/{item}'

    if item.name not in steam_names:
        try:
            # print(item)
            steam_link_to_add = steam_link.format(item=item.name)
            full_page = requests.get(steam_link_to_add).content
            item_nameid = re.findall(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)', str(full_page))[0]
            steamlink_column = 'https://steamcommunity.com/market/itemordershistogram?country=BY&language=russian&currency=1&item_nameid={item_nameid}&two_factor=0'
            list_to_insert.append([item.name, steam_link_to_add.format(item_nameid=item_nameid), item_nameid])
        except Exception as ex:
            print(ex)
            return


def insertToDatabase():
    for item in list_to_insert:
        try:
            cur.execute("""INSERT INTO steaminfo VALUES (%s, %s,%s,%s,%s)""",
                        (item[0], item[1], item[2], None, None))
            conn.commit()
        except Exception as ex:
            print(ex)
