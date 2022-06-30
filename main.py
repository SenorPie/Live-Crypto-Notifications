import os
import requests
from dotenv import load_dotenv
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



if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("COINMARKET_API_KEY")
    CoinMarketWrapper(api_key=api_key).quotes_latest(symbol="SHIB")
