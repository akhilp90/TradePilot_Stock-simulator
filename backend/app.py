from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import pytz  # Library for timezone conversion
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define timezones
est = pytz.timezone("America/New_York")  # U.S. Market timezone (EST/EDT)
ist = pytz.timezone("Asia/Kolkata")  # Indian Standard Time (IST)

# Fetch stock data for a given symbol
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d", interval="5m")  # Get latest 5-min interval data
    
    if not data.empty:
        latest_time_utc = data.index[-1]  # Get latest timestamp (in UTC)
        latest_price = data["Open"].iloc[-1]  # Get latest open price
        
        # Convert timestamp to IST
        latest_time_est = latest_time_utc.tz_convert(est)  # Convert UTC to EST first
        latest_time_ist = latest_time_est.astimezone(ist)  # Convert EST to IST
        
        return {
            'symbol': symbol,
            'price': round(latest_price, 2),
            'time': latest_time_ist.strftime('%Y-%m-%d %H:%M:%S') + ' IST'
        }
    return None

# Endpoint to get top trending stocks
@app.route('/api/stocks')
def get_top_stocks():
    stock_symbols = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'RELIANCE.NS', 'TATAMOTORS.NS', 'INFY', 'HDFC', 'SBIN']
    stock_data = []

    for symbol in stock_symbols:
        data = get_stock_data(symbol)
        if data:
            stock_data.append(data)

    # Sort stocks by price (descending) and get top 6
    sorted_stocks = sorted(stock_data, key=lambda x: x['price'], reverse=True)[:6]

    return jsonify(sorted_stocks)

if __name__ == '__main__':
    app.run(debug=True)
