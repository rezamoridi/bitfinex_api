import requests
from datetime import datetime, timedelta
import time
from tools.time_convert import convert_timesnap
from tools.write_csv import save_to_csv_beta


def get_bitfinex_price_data(symbol, start_date, end_date, timeframe):
    # Convert dates to Unix timestamps
    start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)
    end_timestamp = int((datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).timestamp() * 1000)

    # Bitfinex API endpoint
    url = f"https://api.bitfinex.com/v2/candles/trade:{timeframe}:{symbol}/hist"

    # Parameters
    params = {
        'start': start_timestamp,
        'end': end_timestamp,
        'sort': 1,  # Sort in ascending order by timestamp
        'limit': 1000  # Maximum number of data points per request
    }

    retry_attempts = 3  # Number of retry attempts
    delay = 1  # Initial delay in seconds

    for attempt in range(retry_attempts):
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data
        elif response.status_code == 429:  # Rate limit exceeded
            print(f"Rate limit exceeded. Retry attempt {attempt + 1} in {delay} seconds.")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        else:
            print("Error:", response.status_code)
            return None

    print("Failed after multiple retry attempts.")
    return None




def get_bitfinex_api_ticker(symbol, delay = 0, channel_time = None): # Delay for preventing rate limit 

    

    def fetch_data():
        url = f"https://api-pub.bitfinex.com/v2/ticker/{symbol}"
        response = requests.get(url=url)

        if response:
            if response.status_code == 200:
                data = response.json() + [convert_timesnap(time.time())]
                return data
            if response.status_code == 429:
                print(f"Rate limit exceeded, Retry in {delay} seconds")
            else:  
                return response

    
    if channel_time:    # Channel will hold data for channel_time duration and convert to csv
        data = []
        start_date = time.time()
        end_date = time.time() + channel_time
        while time.time() - 1 < end_date:
            data.append(fetch_data())
        print(f"csv created! - {convert_timesnap(time.time())}")
        return save_to_csv_beta(data_list=data, filename=f"{symbol} - {convert_timesnap(start_date)} - {convert_timesnap(end_date)}.csv")
    else:
        return(fetch_data())

    

    




# ticker usage

"""request = get_bitfinex_api_ticker("tBTCUSD",channel_time=5)"""



# candle Usage  

'''request = get_bitfinex_price_data(symbol='tBTCUSD', start_date='2024-04-20', end_date='2024-04-23', timeframe='1m')
""" timeframe : 1m, 30m ,1h, 1D ..."""

if request:
    save_to_csv(data=request, filename="bitfinex_btc_price.csv")
    print("Success")
else:
    print("Faild to save data")'''

    