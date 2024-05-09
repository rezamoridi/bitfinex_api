import asyncio
import websockets
import json
import csv
from finex.tools import time_convert

async def heartbeat(websocket, interval):
    while True:
        await websocket.send(json.dumps({"method": "SUBSCRIBE", "params": ["btcusdt@kline_1m"], "id": 1}))
        await asyncio.sleep(interval)

async def subscribe_to_ohclv():
    uri = "wss://stream.binance.com:9443/ws"

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                asyncio.create_task(heartbeat(websocket, 5))

                async for message in websocket:
                    data = json.loads(message)

                    if 'k' in data:  # OHLCV data comes in candlestick (kline) format
                        ohlcv = {
                            "timestamp": time_convert.convert_timesnap_time(data['k']['t'] / 1000),  # Convert timestamp to seconds
                            "open": data['k']['o'],
                            "high": data['k']['h'],
                            "low": data['k']['l'],
                            "close": data['k']['c'],
                            "volume": data['k']['v']
                        }
                        write_to_csv(ohlcv)

        except websockets.exceptions.ConnectionClosedError:
            print("Connection to the WebSocket closed unexpectedly. Retrying...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await asyncio.sleep(5)

def write_to_csv(data):
    csv_file = "ohclv_data.csv"

    with open(csv_file, 'a', newline='') as file:
        fieldnames = ["timestamp", "open", "high", "low", "close", "volume"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(data)

asyncio.get_event_loop().run_until_complete(subscribe_to_ohclv())
