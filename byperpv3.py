import telegram
import asyncio
import talib
from bybit import Client

# Replace YOUR_API_TOKEN with your Telegram bot's API token
bot = telegram.Bot(token='YOUR_API_TOKEN')

# Set the chat_id where you want to send the message
chat_id = 12345678

# Set the timeframe (in minutes) for checking the MACD line
timeframe = 15

# Create a Client object for accessing the Bybit API
client = Client()

async def main():
    # Set the previous price to None initially
    previous_price = None

    while True:
        # Get the latest MACD and signal line values for the specified timeframe
        candles = client.candles.get(symbol='BTCUSD', interval=f'{timeframe}m', limit=1)
        data = candles['result'][0]
        macd = data['macd']
        signal = data['signal']

        # Use the crossover function from talib to check if the MACD line has crossed the signal line
        macd_crossed_signal = talib.crossover(macd, signal)

        # Check if the MACD line has crossed the signal line
        if macd_crossed_signal[-1] == 1:
            # MACD line crossed signal line upwards
            direction = 'upwards'
        elif macd_crossed_signal[-1] == -1:
            # MACD line crossed signal line downwards
            direction = 'downwards'
        else:
            # MACD line and signal line are equal, no crossing
            direction = None

        # Check if the price has risen or dropped since the last message
        last_price = data['close']
        if last_price > previous_price:
            # Price has risen
            price_change = 'risen'
        elif last_price < previous_price:
            # Price has dropped
            price_change = 'dropped'
        else:
            # Price has not changed
            price_change = 'not changed'

        # Save the current price as the previous price for the next iteration
        previous_price = last_price

        # If the MACD line crossed the signal line, send a message with the direction and price change
        if direction is not None:
            message = f'MACD line crossed signal line {direction}. Price has {price_change}.'
            bot.send_message(chat_id=chat_id, text=message)

        # Wait one minute before checking again
        await asyncio.sleep(60)

asyncio.run(main())

print("END")
