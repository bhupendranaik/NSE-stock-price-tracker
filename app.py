import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import ttk for Combobox
import yfinance as yf
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')


# Function to fetch stock data (same as before)
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


# Function to plot the chart for stock (same as before)
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

    chart_path = f'{symbol}_chart.png'
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()
    return chart_path


# Function to handle fetching and displaying data
def on_fetch_data():
    symbol = entry_symbol.get().upper().strip()
    period = combo_period.get()

    # Fetch the stock data
    stock_data = fetch_stock_data(symbol, period)

    if stock_data:
        price, day_high, day_low, opening_price, pe_ratio = stock_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Display the data in labels
        label_price.config(text=f"Price: ₹{price}")
        label_day_high.config(text=f"Day High: ₹{day_high}")
        label_day_low.config(text=f"Day Low: ₹{day_low}")
        label_opening_price.config(text=f"Opening Price: ₹{opening_price}")
        label_pe_ratio.config(text=f"P/E Ratio: {pe_ratio if pe_ratio else 'N/A'}")
        label_timestamp.config(text=f"Timestamp: {timestamp}")

        # Plot the stock chart
        chart_path = plot_chart(symbol, period)
        if chart_path:
            img = tk.PhotoImage(file=chart_path)
            label_chart.config(image=img)
            label_chart.image = img  # Keep a reference to the image
    else:
        messagebox.showerror("Error", "Failed to fetch data. Please try again.")


# Set up the Tkinter window
root = tk.Tk()
root.title("NSE Stock Price Tracker")

# Symbol input
label_symbol = tk.Label(root, text="Enter Stock Symbol (e.g., RELIANCE):")
label_symbol.grid(row=0, column=0, padx=10, pady=5)
entry_symbol = tk.Entry(root, width=20)
entry_symbol.grid(row=0, column=1, padx=10, pady=5)

# Period dropdown (using ttk.Combobox)
label_period = tk.Label(root, text="Select Period:")
label_period.grid(row=1, column=0, padx=10, pady=5)
combo_period = ttk.Combobox(root, values=["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y"], width=17)
combo_period.set("1mo")  # Default value
combo_period.grid(row=1, column=1, padx=10, pady=5)

# Fetch button
button_fetch = tk.Button(root, text="Fetch Data", command=on_fetch_data)
button_fetch.grid(row=2, columnspan=2, pady=10)

# Stock data labels
label_price = tk.Label(root, text="Price: ₹0.00")
label_price.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

label_day_high = tk.Label(root, text="Day High: ₹0.00")
label_day_high.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

label_day_low = tk.Label(root, text="Day Low: ₹0.00")
label_day_low.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

label_opening_price = tk.Label(root, text="Opening Price: ₹0.00")
label_opening_price.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

label_pe_ratio = tk.Label(root, text="P/E Ratio: N/A")
label_pe_ratio.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

label_timestamp = tk.Label(root, text="Timestamp: N/A")
label_timestamp.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

# Chart display area
label_chart = tk.Label(root)
label_chart.grid(row=9, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()
