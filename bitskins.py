import re
from concurrent.futures.thread import ThreadPoolExecutor
from socket import socket
import socks
import pyotp
import requests

from Item import BitskinsItem
from models import conn


api_key = '2804b7aa-c08b-4c1a-9336-d08d95ed16b3'

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)

socket.socket = socks.socksocket
bitskins_link = 'https://bitskins.com/api/v1/get_all_item_prices/?api_key=2804b7aa-c08b-4c1a-9336-d08d95ed16b3&app_id=730&code={code}'
cur = conn.cursor()

# Connection to API
code = pyotp.TOTP("EB4HZJ67O6CDUS35").now()
updatedBitskinsItems = []

urlForAutobuy='https://bitskins.com/api/v1/summarize_buy_orders/?api_key=2804b7aa-c08b-4c1a-9336-d08d95ed16b3&app_id=730&code={code}'
bitskinsUrl = 'https://bitskins.com/api/v1/get_price_data_for_items_on_sale/?api_key=2804b7aa-c08b-4c1a-9336-d08d95ed16b3&code={code}&app_id=730'

all_items = requests.get(bitskinsUrl.format(code=code)).json()
allAutobuyItems = requests.post(urlForAutobuy.format(code=code)).json()
autobuyItemsPrices = []

#for autobuy
def updateBitskinsAutobuyPrice(item):
    name = item[0]
    autobuyPrice = item[1]['max_price']
    updatedBitskinsItems.append(
        BitskinsItem(name=name, price=None, autobuyPrice=autobuyPrice))

#for autobuy
def getBitskinsAutobuyPrice():
    with ThreadPoolExecutor(max_workers=100) as executor:
        for item in allAutobuyItems['data']['items']:
            executor.map(updateBitskinsAutobuyPrice, [item])
        executor.shutdown(wait=True)
    return updatedBitskinsItems

#for price
def updateBiskinsPrice(item):

    name = item['market_hash_name']
    price = item['lowest_price']
    if float(price) < 0.03:
        return

    updatedBitskinsItems.append(BitskinsItem(name=name, price=price, autobuyPrice=None))


#for price
def getBitskinsPrice():
    with ThreadPoolExecutor(max_workers=100) as executor:
        for item in all_items['data']['items']:
            executor.map(updateBiskinsPrice, [item])
        executor.shutdown(wait=True)
    return updatedBitskinsItems



#getBitskinsPrice()
#getBitskinsAutobuyPrice()
#print("BITSKINS UPDATING EXIT")