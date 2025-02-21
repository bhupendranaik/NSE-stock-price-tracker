📌 NSE Stock Price Tracker

🚀 Overview
The NSE Stock Price Tracker is a Flask-based web application that allows users to fetch and visualize real-time stock data from the National Stock Exchange (NSE). It provides insights such as closing price, day high & low, opening price, P/E ratio, and also generates stock price trend charts. The data is stored in MySQL and exported to Excel for further analysis.

🔧 Tech Stack
Backend: Python (Flask)
Data Handling: Pandas, Yahoo Finance API (yfinance)
Database: MySQL
Visualization: Matplotlib
Frontend: HTML, CSS
Storage: Excel file

🎯 Features
✅ Fetch real-time stock prices from NSE
✅ Displays closing price, opening price, P/E ratio, day high & low
✅ Saves stock data to MySQL for historical records
✅ Exports stock data to Excel
✅ Generates dynamic stock charts for price trends
✅ User-friendly Flask web interface

📥 Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/NSE-Stock-Price-Tracker.git

2️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Setup MySQL Database
Ensure MySQL is installed and running.
Create a database called stock_data_db.
Update the MySQL credentials in app.py.

🚀 Running the Application
python app.py
The app will be live at http://127.0.0.1:5000/

🖼 Screenshots
💡 (Include some screenshots of your web app interface and stock charts here!)

🛠 Troubleshooting & Common Issues
❌ Stock Data Not Fetching?
Ensure Yahoo Finance API is working:
👉 Open Yahoo Finance in a browser.
Try upgrading yfinance:
bash
Copy
Edit
pip install --upgrade yfinance

❌ MySQL Connection Issue?
Ensure MySQL service is running
Double-check username, password, and database name in app.py

🎯 Future Enhancements
🔹 Add historical stock data analysis 📊
🔹 Implement AI-based stock predictions 🤖
🔹 Add technical indicators (RSI, Moving Averages, etc.)

🤝 Contributing
Contributions are welcome! Feel free to fork this repo, create a feature branch, and submit a PR.

🚀 Let's Connect!
💡 If you like this project, give it a ⭐ on GitHub!
📩 Feel free to reach out for collaboration opportunities.
