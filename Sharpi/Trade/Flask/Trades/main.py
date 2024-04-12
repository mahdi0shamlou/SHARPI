import time
import requests
import hmac
from hashlib import sha256
import json
APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""
APIKEY = "V1WB8ZbcLxxNQXeGmFIyIfsOXilEml2PQtPvNeoG7NQ3kvHE0kSmHojh6QTmzzNIyhxdBERX9cCTRfqkVkcA"
SECRETKEY = "jmiA7wmjlIHZyJ3kQdkIS5x329dyQijywgcAXxyvIGRlYTCfM1JC8Wus5swqhddTgcWXYqw1lf9SCC1X1EDQ"
def demo_list_open_order():
    url = "https://open-api.bingx.com/openApi/v2/common/server/time"
    headers = {'x-api-key': '09ba90f6-dcd0-42c0-8c13-5baa6f2377d0'}
    resp = requests.get(url, headers=headers)
    x = resp.json()
    timestamp = x['timestamp']
    payload = {}
    path = '/openApi/swap/v2/trade/openOrders'
    method = "GET"
    paramsMap = {
    "symbol": "BTC-USDT",
    "timestamp": timestamp
    }

    paramsStr = parseParam_cancel(paramsMap)
    x = send_request_cancel(method, path, paramsStr, payload)
    x = json.loads(x)
    for i in x['data']['orders']:
        print("demo:", i['orderId'])
    return x['data']['orders']

def demo_list_open_order_eth():
    url = "https://open-api.bingx.com/openApi/v2/common/server/time"
    headers = {'x-api-key': '09ba90f6-dcd0-42c0-8c13-5baa6f2377d0'}
    resp = requests.get(url, headers=headers)
    x = resp.json()
    timestamp = x['timestamp']
    payload = {}
    path = '/openApi/swap/v2/trade/openOrders'
    method = "GET"
    paramsMap = {
    "symbol": "ETH-USDT",
    "timestamp": timestamp
    }

    paramsStr = parseParam_cancel(paramsMap)
    x = send_request_cancel(method, path, paramsStr, payload)
    x = json.loads(x)
    for i in x['data']['orders']:
        print("demo:", i['orderId'])
    return x['data']['orders']
def get_sign_cancel(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature
def send_request_cancel(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign_cancel(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text
def parseParam_cancel(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "":
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))

if __name__ == '__main__':
    x = demo_list_open_order()
    print("demo:", demo_list_open_order())
    x = json.loads(x)

    for i in x['data']['orders']:
        print("demo:", i['orderId'])