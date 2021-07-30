import asyncio
import socket
import time
from concurrent.futures.thread import ThreadPoolExecutor
from xml.etree.ElementTree import fromstring

from toripchanger import TorIpChanger
import requests


import requests
import socks

from Item import SteamItem
from bitskins import getBitskinsAutobuyPrice, getBitskinsPrice
from models import cur, conn

proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket

headers = {u"User-Agent": u"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 OPR/18.0.1284.68"}
ITEMORDERSHESTOGRAM_LINK = u"https://steamcommunity.com/market/itemordershistogram?country=BY&language=russian&currency=1&item_nameid={nameid}&two_factor=0"

cur.execute("SELECT name, steamlink, steamid, price FROM steaminfo WHERE price::decimal > 0.1 AND NAME NOT LIKE '★%'")  # WHERE price::decimal > 0.1 AND NAME NOT LIKE '★%'
rows = cur.fetchall()

updatedSteamItems = []
bitskinsToSteamAutobuyItems = []

steamItems = []




def fetch(session, row):
    with session.get(ITEMORDERSHESTOGRAM_LINK.format(nameid=row[2])) as response:
        try:
            full_page = response.json()
            steamPrice = float(full_page['lowest_sell_order'])
            steamAutobuyPrice = float(full_page['highest_buy_order'])
            steamItem = SteamItem(id=row[2], name=row[0], price=steamPrice / 100, autobuyPrice=steamAutobuyPrice / 100)
            steamItems.append(steamItem)
            print(steamItem)
            updateData(steamItem)
        except Exception as ex:
            print(ex + ' ' + response.status_code)

            return


def updateData(SteamItem):
    try:
        cur.execute("""UPDATE steaminfo SET PRICE = %s, AUTOBUY_PRICE = %s WHERE name = %s""",
                    (str(SteamItem.price), str(SteamItem.autobuyPrice), str(SteamItem.name),))
        conn.commit()
    except Exception as ex:
        print(ex)


def bitskinsToSteamAutobuy():
    updatedBitskinsItems = getBitskinsPrice()

    for steamItem in steamItems:
        try:
            for bitskinsItem in updatedBitskinsItems:
                if steamItem.name == bitskinsItem.name:
                    bitskinsToSteamAutobuyItems.append([steamItem.name,

                                                        float(bitskinsItem.price),
                                                        float(steamItem.autobuyPrice)
                                                        ])
        except:
            continue
    bitskinsToSteamAutobuyItems.sort(key=lambda x: x[1] / x[2], reverse=True)
    for item in bitskinsToSteamAutobuyItems:
        print(str(item[0]) + ' ' + str(item[1]) + ' ' + str(item[2]) + ' ' + str(100 - item[1] / item[2] * 100))


def bitskinsAutobuyToSteam():
    updatedBitskinsItems = getBitskinsAutobuyPrice()
    for steamItem in steamItems:
        try:
            for bitskinsItem in updatedBitskinsItems:
                if steamItem.name == bitskinsItem.name:
                    bitskinsToSteamAutobuyItems.append([steamItem.name,

                                                        float(bitskinsItem.autobuyPrice),
                                                        float(steamItem.price)
                                                        ])
        except Exception as ex:
            continue
    bitskinsToSteamAutobuyItems.sort(key=lambda x: x[1] / x[2])
    for item in bitskinsToSteamAutobuyItems:
        print(item[0] + ' ' + str(item[1]) + ' ' + str(item[2]) + ' ' + str(100 - item[1] / item[2] * 100))


async def comparing():

    with ThreadPoolExecutor(max_workers=50) as executor:
        with requests.Session() as session:
            for row in rows:

                executor.map(fetch, [session], [row])
            executor.shutdown(wait=True)
        print("STEAM UPDATING EXIT")
    bitskinsToSteamAutobuy()
    #bitskinsAutobuyToSteam()



if __name__ == "__main__":
    start_time = time.time()
    #start()
    comparing()
    print("--- %s seconds ---" % (time.time() - start_time))
    conn.commit()
    conn.close()
