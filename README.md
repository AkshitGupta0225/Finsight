📈 FinSight – Intelligent Stock Portfolio Analyzer

A modern, ML-powered, interactive stock analytics and portfolio management app built with Streamlit, yfinance, SQLite, Plotly, Finnhub API, scikit-learn, and a custom floating AI advisor.

🚀 Features
✅ 1. User Authentication

Secure login & registration system

Password hashing using bcrypt

Password reset functionality

✅ 2. Multi-Portfolio Management

Create multiple portfolios

Add or remove stocks

Track shares, buy price, market value, and PnL

Export portfolio as CSV or Excel

✅ 3. Interactive Dashboard

Live price tracking

Dynamic trend charts (6 months, 1 year, 2 years)

Profit/Loss pie charts

Portfolio growth timeline

✅ 4. Global Live Ticker Bar

A beautiful animated ticker showing 25 real-time stock price changes with colored price movement indicators.

✅ 5. Price Alerts

Set alerts for:

% price movement

Up, down, or any movement

Optional email notifications using SMTP

Alerts trigger automatically and display in app.

✅ 6. Watchlist with Live Charts

Select stocks to watch

Mini sparkline charts

1-year candlestick detailed chart

✅ 7. Risk & Correlation Analytics

Includes:

Sharpe Ratio

Beta vs benchmark

Annualized volatility

Correlation heatmap (for all portfolio stocks)

✅ 8. Sector Allocation & Concentration

Smart sector detection (via yfinance and fallback mapping)

Pie chart of allocation

Treemap of holdings

Concentration risk warnings

✅ 9. Benchmark Comparison

Compare individual stocks with:

S&P 500

NIFTY 50

Sensex

Performance normalized to index = 100.

✅ 10. Crypto Analytics

Supports:

BTC, ETH, SOL, XRP
Shows:

Volatility

Sparkline chart

Returns

Close price timeline

✅ 11. Market News + Sentiment Analysis

Using Finnhub API:

Latest company news

Clickable headlines

Sentiment score (Positive / Neutral / Negative)

Progress bar for compound sentiment score

✅ 12. ML-Powered Stock Advisor

Machine Learning model using:

Random Forest Classifier

5-year historical stock data

Technical indicators: RSI, EMA, MACD, SMA ratios, volatility

Predicts 🔮
“BUY” or “AVOID” along with probability

Displays:

Accuracy

ROC AUC

Precision & Recall

Predictions for each selected stock

✅ 13. Floating AI Chatbot

A sleek interactive chatbot providing:

Risk tips

Diversification guidance

Quick momentum hints

Basic sentiment interpretation

Always visible in bottom-right corner.

✅ 14. Theme Toggle (Dark / Light Mode)

Dynamic theme switching using custom CSS.

🛠️ Tech Stack
Frontend

Streamlit

Custom CSS

Plotly (interactive charts)

Backend

Python

SQLite (users, portfolios, alerts)

Finnhub API (news)

yfinance (stock & crypto data)

Machine Learning

scikit-learn (Random Forest, TimeSeriesSplit)

Feature engineering (RSI, SMA, MACD, volatility)

📦 Requirements
streamlit
yfinance
pandas
numpy
plotly
sqlite3
bcrypt
finnhub-python
vaderSentiment
scikit-learn
requests

▶️ How to Run

Clone the repository:

git clone <repo-url>
cd finsight


Install dependencies:

pip install -r requirements.txt


Run the app:

streamlit run g.py


(Optional) Add SMTP credentials to .streamlit/secrets.toml:

smtp_host="smtp.gmail.com"
smtp_port=587
smtp_user="your_email@gmail.com"
smtp_pass="your_password"
from_email="your_email@gmail.com"

📚 Folder Structure
/FinSight
│── g.py                 # Main Streamlit app
│── users.db             # User login database
│── portfolio.db         # Stocks & portfolio data
│── requirements.txt
│── README.md

🤝 Contributions

Pull requests are welcome—especially improvements to:

ML model

UI/UX

Crypto analytics

Advisor logic
