import asyncio
import websockets
import json
import time

async def heartbeat(websocket, interval):
    while True:
        await websocket.send(json.dumps({"event": "ping"}))  # Send a heartbeat message
        await asyncio.sleep(interval)  # Wait for the next heartbeat interval

async def subscribe_to_ticker():
    uri = "wss://api-pub.bitfinex.com/ws/2"

    async with websockets.connect(uri) as websocket:
        # Subscribe to the ticker channel for BTC/USD pair
        await websocket.send('{"event": "subscribe", "channel": "ticker", "symbol": "tBTCUSD"}')

        # Start the heartbeat task with a shorter interval (e.g., 5 seconds)
        asyncio.create_task(heartbeat(websocket, 1))

        datas = {}
        # Receive and process messages
        async for message in websocket:
            # Parse the JSON message
            data = json.loads(message)

            
            # Check if it's a ticker update message
            if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list) and len(data[1]) > 6:
                # Extract the last price from the ticker update
                last_price = data[1][0]
                last_avg = {last_price: last_price/2}
                print(f"Last price of BTC/USD: {last_avg}")

# Run the WebSocket client
asyncio.get_event_loop().run_until_complete(subscribe_to_ticker())
