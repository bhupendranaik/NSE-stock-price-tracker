

##### welcome to my project : NSE stock price tracker  ######

from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import mysql.connector
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

# This Function used to fetch stock data including P/E ratio
def fetch_stock_data(symbol, period='1mo'):
    try:
        stock = yf.Ticker(symbol + ".NS")
        hist = stock.history(period=period)
        if hist.empty:
            return None
        price = round(hist['Close'].iloc[-1], 2)  # Closing price of the most recent day
        day_high = round(hist['High'].max(), 2)  # Max high within the selected period
        day_low = round(hist['Low'].min(), 2)  # Min low within the selected period
        opening_price = round(hist['Open'].iloc[0], 2)  # Opening price on the first day
        pe_ratio = round(stock.info['trailingPE'], 2) if 'trailingPE' in stock.info else None  # P/E ratio
        return price, day_high, day_low, opening_price, pe_ratio
    except Exception as e:
        return None

# Function to save data to MySQL
def save_to_sql(data):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="football@265",
        database="stock_data_db"
    )
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock_data (
                        Symbol VARCHAR(10),
                        Price FLOAT,
                        Day_High FLOAT,
                        Day_Low FLOAT,
                        Opening_Price FLOAT,
                        PE_Ratio FLOAT,
                        Timestamp DATETIME
                      )''')
    cursor.execute(
        "INSERT INTO stock_data (Symbol, Price, Day_High, Day_Low, Opening_Price, PE_Ratio, Timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (data['Symbol'], data['Price'], data['Day_High'], data['Day_Low'], data['Opening_Price'], data['PE_Ratio'], data['Timestamp'])
    )
    conn.commit()
    cursor.close()
    conn.close()


# Function to save stock data to Excel file
def save_to_excel(data):
    # Path to the Excel file
    excel_file_path = 'stock_data.xlsx'

    # Check if the file exists
    if os.path.exists(excel_file_path):
        # If file exists, we load it
        with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            # Load the existing Excel file
            df_existing = pd.read_excel(excel_file_path, sheet_name='StockData')
            # Create a DataFrame from the new data
            df_new = pd.DataFrame([data])
            # Append the new data to the existing DataFrame
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            # Write the updated DataFrame back to the file
            df_combined.to_excel(writer, sheet_name='StockData', index=False)
    else:
        # If file does not exist, create a new one
        df_new = pd.DataFrame([data])
        with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
            df_new.to_excel(writer, sheet_name='StockData', index=False)


# Function to plot the chart for stock
def plot_chart(symbol, period):
    stock = yf.Ticker(symbol + ".NS")
    hist = stock.history(period=period)
    if hist.empty:
        return None

    plt.figure(figsize=(10, 5))
    plt.clf()  # Clear the current figure
    hist['Close'].plot()
    plt.title(f"Stock Price for {symbol} ({period})")
    plt.xlabel("Date")
    plt.ylabel("Price (₹)")
    plt.xticks(rotation=45)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    chart_path = f'static/images/{symbol}_chart.png'
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()
    return chart_path

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form['symbol'].upper().strip()
        period = request.form.get('period', '1mo')
        stock_data = fetch_stock_data(symbol, period)

        if stock_data:
            price, day_high, day_low, opening_price, pe_ratio = stock_data
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {
                'Symbol': symbol,
                'Price': price,
                'Day_High': day_high,
                'Day_Low': day_low,
                'Opening_Price': opening_price,
                'PE_Ratio': pe_ratio,
                'Timestamp': timestamp
            }
            save_to_sql(data)  # Save to MySQL
            save_to_excel(data)  # Save to Excel
            chart_path = plot_chart(symbol, period)

            return render_template('index.html', symbol=symbol, price=price, day_high=day_high,
                                   day_low=day_low, opening_price=opening_price, pe_ratio=pe_ratio,
                                   timestamp=timestamp, chart_path=chart_path, period=period)
        else:
            return render_template('index.html', error="Failed to fetch data. Please try again.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
