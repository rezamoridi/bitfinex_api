import requests

url = "https://api-pub.bitfinex.com/v2/tickers?symbols=tBTCUSD"

response = requests.get(url=url)

print(response.json())