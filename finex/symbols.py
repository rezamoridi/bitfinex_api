import requests

response = requests.get(url="https://api-pub.bitfinex.com/v2/conf/pub:list:pair:exchange")

symbols = sorted(list(response.json()[0]))
