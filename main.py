import os
import threading
import requests
from dotenv import load_dotenv
from win10toast import ToastNotifier
from time import sleep
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

class CoinMarketWrapper:
    def __init__(self, api_key):
        self.coinmarket_url = "https://pro-api.coinmarketcap.com/v2"
        self.session = requests.session()

        self.session.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }
    
    def quotes_latest(self, symbol="BTC"):
        url = f"{self.coinmarket_url}/cryptocurrency/quotes/latest"

        params = {
            "symbol": symbol
        }

        try:
            response = self.session.get(url=url, params=params)
            data = response.json()['data']
            
            # Query through all keys
            for key in data[symbol]:
                return key.get('quote').get('USD')
            
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)


class CryptoLiveNotify:
    def __init__(self):
        load_dotenv()
        self.coinmarket_api = CoinMarketWrapper(api_key=os.getenv("COINMARKET_API_KEY"))
        self.toaster = ToastNotifier()

    def main(self):
        current_threads = {}

        while True:
            print("| Crypto Live Notifications |")
            print("| !exit to stop the program |") 
            print("| !add to watch new crypto  |")
            print("| !remove to stop watching  |")
            print("| !list to see current list |")

            cmd = input(">> ")

            if cmd == "!exit":
                if len(current_threads) > 0:
                    for thread in current_threads.values():
                        thread.terminate()
                break

            elif cmd == "!add":
                symbol = input("Crypto symbol (BTC) to add: ")
                notify_price = int(input("What price should we notify you on? "))
                sleep_time = float(input("What time do you want to sleep for between requests? "))

                new_thread = PriceCheckThread(coinmarket_api=self.coinmarket_api,
                                              symbol=symbol,
                                              notify_price=notify_price,
                                              sleep_time=sleep_time,
                                              win_notify=self.toaster)

                current_threads.update({symbol: new_thread})
                new_thread.start()

            elif cmd == "!remove":
                symbol = input("Crypto symbol (BTC) to remove: ")
                thread = current_threads.get(symbol)
                if thread:
                    thread.terminate()
                    current_threads.pop(symbol)

            elif cmd == "!list":
                print(current_threads) 

class PriceCheckThread(threading.Thread):
        def __init__(self, coinmarket_api, symbol, notify_price, sleep_time, win_notify=None):
            super().__init__()
            self.keep_alive = True
            self.coinmarket_api = coinmarket_api
            self.win_notify = win_notify
            self.symbol = symbol
            self.notify_price = notify_price
            self.sleep_time = sleep_time
        
        def terminate(self):
            self.join()
            self.keep_alive = False

        def run(self):
            while self.keep_alive:
                latest_quote = self.coinmarket_api.quotes_latest(symbol=self.symbol)
                price = int(latest_quote.get('price'))
                if price > self.notify_price:
                    print(f"PRICE HAS INCREASED ABOVE {self.notify_price}")
                    
                    if type(self.win_notify) is not None:
                        self.win_notify.show_toast("Crypto Notification", f"{self.symbol} has gone above the price of {self.notify_price}")

                sleep(self.sleep_time)


if __name__ == "__main__":
    CryptoLiveNotify().main()