import requests
import csv

def fetch_symbols(symbols_list : list = None, heads : list = None) -> bool:

    if symbols_list and heads:
        symbols = symbols_list
        headers = heads
    else:
        response = requests.get(url="https://api-pub.bitfinex.com/v2/conf/pub:list:pair:exchange")
        headers = ['Symbols']
        symbols = response.json()[0]

    with open("../csv/symbols_csv/symbolcsv.csv", mode="+w") as symbolcsv:
        writer = csv.writer(symbolcsv)

        writer.writerow(headers)
        for symbol in symbols:
            writer.writerow([symbol])
    
    return True

if __name__ == "__main__":
    fetch_symbols()
