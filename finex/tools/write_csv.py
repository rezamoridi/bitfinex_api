import csv
from datetime import datetime

from .time_convert import convert_timesnap 

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])
        for candle in data:
            timestamp = datetime.fromtimestamp(int(candle[0]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            open_price = candle[1]
            high_price = candle[3]
            low_price = candle[4]
            close_price = candle[2]
            volume = candle[5]
            writer.writerow([timestamp, open_price, high_price, low_price, close_price, volume])


def save_to_csv_beta(data_list, filename):
    headers = ["BID", "BID_SIZE", "ASK", "ASK_SIZE", "DAILY_CHANGE", "DAILY_CHANGE_PERCENT", "LAST_PRICE", "VOLUME", "HIGH", "LOW", "TIMESTAMP"]
    with open(file=f"csv/ticker_csv/{filename}", mode="a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for record in data_list:
            writer.writerow(record)