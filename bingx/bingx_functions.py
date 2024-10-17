import time
import requests
import hmac
from hashlib import sha256
import json
from databases.db_coin_functions import add_coin_db

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""


# ---------------------------------------------------------------------------------------
# Три Функции которые отвечают за валидные монетки bingX испольхуются только в coin_chaker
def all_coins():
    payload = {}
    path = '/openApi/spot/v1/common/symbols'
    method = "GET"
    paramsMap = {
    }
    paramsStr = parseParam(paramsMap)
    return json.loads(send_request(method, path, paramsStr, payload))


def all_coins_correct(i):
    payload = {}
    path = '/openApi/spot/v1/market/depth'
    method = "GET"
    paramsMap = {
        "symbol": i,
        "limit": 5
    }
    paramsStr = parseParam(paramsMap)
    return json.loads(send_request(method, path, paramsStr, payload))


def get_all_coins():
    for i in all_coins()['data']['symbols']:
        answer = all_coins_correct(i['symbol'])
        if answer['code'] == 0:
            add_coin_db(i['symbol'].replace('-USDT', ''), "bingx")


# ---------------------------------------------------------------------------------------

# Функция которая возвращает баланс USDT на бирже bingx
def get_balance_usdt_bingx():
    payload = {}
    path = '/openApi/spot/v1/account/balance'
    method = "GET"
    paramsMap = {
        "recvWindow": "60000",
        "timestamp": str(int(time.time() * 1000))
    }
    paramsStr = parseParam(paramsMap)
    for balance in json.loads(send_request(method, path, paramsStr, payload))['data']['balances']:
        if balance['asset'] == 'USDT':
            return balance['free']


# def get_all_deposit_address_bingx():
#     payload = {}
#     path = '/openApi/wallets/v1/capital/config/getall'
#     method = "GET"
#     paramsMap = {
#         "coin": "SOL",
#         "timestamp": str(int(time.time() * 1000))
#     }
#     paramsStr = parseParam(paramsMap)
#     print(send_request(method, path, paramsStr, payload))


# ---------------------------------------------------------------------------------------
# Три функции которые отвечают за подписи и все такое для apiшки их не трогать
def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text


def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "":
        return paramsStr + "&timestamp=" + str(int(time.time() * 1000))
    else:
        return paramsStr + "timestamp=" + str(int(time.time() * 1000))
# ---------------------------------------------------------------------------------------

# demo()
# get_all_deposit_address_bingx()
# if __name__ == '__main__':
#     get_balance_usdt_bingx()
