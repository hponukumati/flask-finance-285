from flask import Flask, request, render_template
import yfinance as yf
from datetime import datetime
import requests

app = Flask(__name__)

def fetch_stock_data(symbol):
    try:
        requests.get("http://www.google.com", timeout=5)
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        if hist.empty:
            return "Error: Symbol not found or no data available."

        company_name = stock.info.get('longName', 'Company name not available')
        current_price = hist['Close'].iloc[-1]
        previous_close = hist['Open'].iloc[-1]
        change = current_price - previous_close
        percent_change = (change / previous_close) * 100

        current_time = datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")
        sign = "+" if change > 0 else "-"
        return f"{current_time}\n\n{company_name} ({symbol})\n\n{current_price:.2f} {sign}{abs(change):.2f} ({sign}{abs(percent_change):.2f}%)"
    except requests.ConnectionError:
        return "Error: Network problem. Please check your internet connection."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def home():
    stock_data = None
    if request.method == 'POST':
        symbol = request.form['symbol']
        stock_data = fetch_stock_data(symbol)
    return render_template('index.html', stock_data=stock_data)

if __name__ == '__main__':
    app.run(debug=True)
