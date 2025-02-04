from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import requests
from flask import Flask, jsonify

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

API_KEY = 'T6U94XS18PG9YGKX'

# Fetch stock data for a given symbol
def get_stock_data(symbol):
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '5min',  # 5-minute interval for real-time data
        'apikey': API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "Time Series (5min)" in data:
            latest_time = list(data["Time Series (5min)"].keys())[0]
            stock_info = data["Time Series (5min)"][latest_time]
            return {
                'symbol': symbol,
                'price': float(stock_info["1. open"]),  # Open price at that time
                'time': latest_time
            }
    return None

# Endpoint to get top trending stocks (dynamically)
@app.route('/api/stocks')
def get_top_stocks():
    # List of stock symbols which are monitored
    stock_symbols = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'RELIANCE.NS', 'TATAMOTORS.NS', 'INFY', 'HDFC', 'SBIN']
    stock_data = []

    # Fetch stock data for each symbol
    for symbol in stock_symbols:
        data = get_stock_data(symbol)
        if data:
            stock_data.append(data)

    # Sort stock data by price (descending)
    sorted_stocks = sorted(stock_data, key=lambda x: x['price'], reverse=True)

    # Get the top 6 stocks
    top_6_stocks = sorted_stocks[:6]
    
    return jsonify(top_6_stocks)

if __name__ == '__main__':
    app.run(debug=True)
