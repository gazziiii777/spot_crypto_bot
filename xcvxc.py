import time
import requests
import hmac
from hashlib import sha256
import json

APIURL = "https://open-api.bingx.com"
APIKEY = "qirnnCIdxmafq5PumDyk0m48hdsgK9fD2jbGqkhGKUrXH43H1AZKw65HtdvHJLQpmNMPL7RIyQaXfIbrA"
SECRETKEY = "jdikCEZONpIOIREfbt5i1I0GFYnF0pZnc1ilOxtF1lPoY2ApsTqPqsjd7poEu9kg3rzQr5BhzDL5UFzdWjg"
str(int(time.time() * 1000))

def demo():
    payload = {}
    path = '/openApi/spot/v1/market/depth'
    method = "GET"
    paramsMap = {
        "symbol": "BLAZE-USDT",
        "limit": 5
    }
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)


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


print("Ордера на покупку", json.loads(demo())["data"]["bids"])
print("Оредра на продажу", json.loads(demo())["data"]["asks"])
