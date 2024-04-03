import time
import requests
import hmac
from hashlib import sha256
import json
APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""
def api_set_key(rr):
    if rr == 2:
        APIKEY = "V1WB8ZbcLxxNQXeGmFIyIfsOXilEml2PQtPvNeoG7NQ3kvHE0kSmHojh6QTmzzNIyhxdBERX9cCTRfqkVkcA"
        SECRETKEY = "jmiA7wmjlIHZyJ3kQdkIS5x329dyQijywgcAXxyvIGRlYTCfM1JC8Wus5swqhddTgcWXYqw1lf9SCC1X1EDQ"
    else:
        APIKEY = "V1WB8ZbcLxxNQXeGmFIyIfsOXilEml2PQtPvNeoG7NQ3kvHE0kSmHojh6QTmzzNIyhxdBERX9cCTRfqkVkcA"
        SECRETKEY = "jmiA7wmjlIHZyJ3kQdkIS5x329dyQijywgcAXxyvIGRlYTCfM1JC8Wus5swqhddTgcWXYqw1lf9SCC1X1EDQ"