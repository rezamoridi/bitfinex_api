import asyncio
import websockets
import json

async def heartbeat(websocket, interval):
    while True:
        await websocket.send(json.dumps({"event": "ping"}))  # Send a heartbeat message
        await asyncio.sleep(interval)  # Wait for the next heartbeat interval

async def subscribe_to_ticker():
    uri = "wss://ws.bitstamp.net"

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                # Subscribe to the ticker channel for BTC/USD pair
                await websocket.send(json.dumps({"event": "bts:subscribe", "data": {"channel": "live_trades_btcusd"}}))

                # Start the heartbeat task with a shorter interval (e.g., 5 seconds)
                asyncio.create_task(heartbeat(websocket, 1))

                # Receive and process messages
                async for message in websocket:
                    # Parse the JSON message
                    data = json.loads(message)

                    # Check if it's a live trades message
                    if 'data' in data and 'amount' in data['data'] and 'price' in data['data']:
                        amount = data['data']['amount']
                        price = data['data']['price']
                        print(f"Last trade: {amount} BTC at ${price} USD")
        except websockets.exceptions.ConnectionClosedError:
            print("Connection to the WebSocket closed unexpectedly. Retrying...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Add a delay before reconnecting
            await asyncio.sleep(5)

# Run the WebSocket client
asyncio.get_event_loop().run_until_complete(subscribe_to_ticker())
