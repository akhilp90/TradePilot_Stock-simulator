from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import pytz  
from datetime import datetime

app = Flask(__name__)
CORS(app)

est = pytz.timezone("America/New_York")  
ist = pytz.timezone("Asia/Kolkata")  

CRYPTO_DETAILS = {
    "BTC-USD": {"symbol": "BTC", "name": "Bitcoin"},
    "ETH-USD": {"symbol": "ETH", "name": "Ethereum"},
    "BNB-USD": {"symbol": "BNB", "name": "Binance Coin"},
    "SOL-USD": {"symbol": "SOL", "name": "Solana"},
    "XRP-USD": {"symbol": "XRP", "name": "XRP"},
    "ADA-USD": {"symbol": "ADA", "name": "Cardano"},
    "DOGE-USD": {"symbol": "DOGE", "name": "Dogecoin"},
    "DOT-USD": {"symbol": "DOT", "name": "Polkadot"},
    "MATIC-USD": {"symbol": "MATIC", "name": "Polygon"},
    "LTC-USD": {"symbol": "LTC", "name": "Litecoin"}
}

def get_crypto_data(symbol):
    crypto = yf.Ticker(symbol)
    data = crypto.history(period="1d", interval="5m")  

    if not data.empty:
        latest_price = data["Open"].iloc[-1]  
        latest_time_utc = data.index[-1]  

        latest_time_est = latest_time_utc.tz_convert(est)  
        latest_time_ist = latest_time_est.astimezone(ist)  

        return {
            'symbol': CRYPTO_DETAILS[symbol]["symbol"],  
            'name': CRYPTO_DETAILS[symbol]["name"],  
            'price': round(latest_price, 2),
            'time': latest_time_ist.strftime('%Y-%m-%d %H:%M:%S') + ' IST'
        }
    return None

# Endpoint to fetch top cryptocurrencies
@app.route('/api/crypto')
def get_top_cryptos():
    crypto_symbols = list(CRYPTO_DETAILS.keys())  
    crypto_data = [get_crypto_data(symbol) for symbol in crypto_symbols if get_crypto_data(symbol)]

    sorted_cryptos = sorted(crypto_data, key=lambda x: x['price'], reverse=True)[:6]

    return jsonify(sorted_cryptos)

if __name__ == '__main__':
    app.run(port=5001, debug=True)  
