import time
import requests
import hmac
from hashlib import sha256
import json

APIKEY = ""
SECRETKEY = ""
class Assets:
    def __init__(self, rr):
        self.APIURL = "https://open-api.bingx.com"
        if rr == 2:
            self.APIKEY = "V1WB8ZbcLxxNQXeGmFIyIfsOXilEml2PQtPvNeoG7NQ3kvHE0kSmHojh6QTmzzNIyhxdBERX9cCTRfqkVkcA"
            self.SECRETKEY = "jmiA7wmjlIHZyJ3kQdkIS5x329dyQijywgcAXxyvIGRlYTCfM1JC8Wus5swqhddTgcWXYqw1lf9SCC1X1EDQ"
        else:
            self.APIKEY = "WXV8KaA9JVSThgTTyGGNiSPApI5W6L5QoUMmZdJTUy9sLi4pzVYlpYGywwAbcU5XohhI9TAZyomfS3MUY0SQ"
            self.SECRETKEY = "n4wHoZKKB8DdxsdMmRoZEYsuAeel88b3x7j8bj3r7dNGravqpUo3JdYrbGMhWSQSVUt8TvWsmIuzc57copYbA"
    def demo(self):
        url = "https://open-api.bingx.com/openApi/v2/common/server/time"
        headers = {'x-api-key': '09ba90f6-dcd0-42c0-8c13-5baa6f2377d0'}
        resp = requests.get(url, headers=headers)
        x = resp.json()
        timestamp = x['timestamp']
        payload = {}
        path = '/openApi/swap/v2/user/balance'
        method = "GET"
        paramsMap = {
        "timestamp": timestamp
    }
        paramsStr = self.parseParam(paramsMap)
        return self.send_request(method, path, paramsStr, payload)

    def get_sign(self, api_secret, payload):
        signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
        print("sign=" + signature)
        return signature


    def send_request(self, method, path, urlpa, payload):
        url = "%s%s?%s&signature=%s" % (self.APIURL, path, urlpa, self.get_sign(self.SECRETKEY, urlpa))
        print(url)
        headers = {
            'X-BX-APIKEY': self.APIKEY,
        }
        response = requests.request(method, url, headers=headers, data=payload)
        return response.text

    def parseParam(self, paramsMap):
        sortedKeys = sorted(paramsMap)
        paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
        if paramsStr != "":
         return paramsStr+"&timestamp="+str(int(time.time() * 1000))
        else:
         return paramsStr+"timestamp="+str(int(time.time() * 1000))
    def start(self):
        resp_assets = self.demo()
        Assets_list = json.loads(resp_assets)

        Assets_list['data']['balance']['unrealizedProfit'] = float(Assets_list['data']['balance']['unrealizedProfit'])
        Assets_list['data']['balance']['realisedProfit'] = float(Assets_list['data']['balance']['realisedProfit'])

        print(Assets_list['data']['balance'])
        return Assets_list['data']['balance']

if __name__ == '__main__':
    obj_assets = Assets(1)
    obj_assets.start()