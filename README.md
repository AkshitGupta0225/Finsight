<div align="center">

# 🌟 **FinSight**
### **AI-Powered Investment Intelligence Dashboard**

A modern portfolio analytics platform featuring  
**real-time market data, ML predictions, news sentiment, crypto analytics, deep portfolio insights, and an on-screen AI financial assistant.**  
Built entirely with **Streamlit + Python**.

---

<img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge">
<img src="https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge">
<img src="https://img.shields.io/badge/Finance-Analytics-0A2540?style=for-the-badge">
<img src="https://img.shields.io/badge/AI-Advisor-6A5ACD?style=for-the-badge">
<img src="https://img.shields.io/badge/ML-Predictions-34D399?style=for-the-badge">

---

### **A cleaner, smarter, dynamic way to understand your investments.**

</div>

---

## 🚀 **Overview**

FinSight is more than a stock tracker — it’s an **intelligent investment command center**.

It blends:

- Real-time stock and crypto insights  
- Multi-portfolio tracking  
- AI-driven recommendations  
- Automated risk analytics  
- Sector & diversification intelligence  
- A floating advisor chatbot  
- A 25-stock animated ticker bar  

All inside a beautifully engineered Streamlit UI with dark/light modes.

---

# ✨ **Core Features**

## **1. Authentication & User System**
- Secure login / register / password reset  
- bcrypt hashed passwords  
- Multi-portfolio support  

---

## **2. Portfolio Intelligence Dashboard**
- Live PnL tracking  
- Current price auto-fetch  
- Trend charts (6m, 1y, 2y)  
- Profit vs loss insight  
- Export to CSV/Excel  

---

## **3. Animated Global Ticker Bar**
A financial-news style moving ticker showing  
**25 major stocks with auto-colored performance indicators**.

---

## **4. Price Alerts Engine**
Create alerts for:
- % price change  
- Direction (up/down/any)  
- Optional email notifications  

---

## **5. Watchlist + Sparkline Trends**
- Quick-view mini charts  
- Auto-updated price & change  
- 1-year Candlestick deep charts  

---

## **6. Risk Analytics**
Professional portfolio risk suite:
- Sharpe Ratio  
- Beta vs indices  
- Annualized volatility  
- Correlation heatmap  

---

## **7. Sector Allocation**
Visual diversification:
- Allocation pie  
- Hierarchical treemap  
- Over-concentration detection  

---

## **8. Benchmark Comparison**
Compare your stocks against:
- S&P 500  
- NIFTY 50  
- Sensex  

Performance normalized to 100 for clarity.

---

## **9. Crypto Dashboard**
Supports: **BTC, ETH, SOL, XRP**

Metrics include:
- Returns  
- Annualized volatility  
- Full price charts  

---

## **10. Market News + Sentiment**
Powered by Finnhub API:

- Latest company news  
- Summaries  
- Sentiment classification  
- Clickable headlines  

---

## **11. Machine Learning Advisor**
A Random Forest model trained on 5 years of data:

- SMA ratios  
- MACD  
- RSI  
- Volatility  
- Daily/weekly returns  

Outputs:
- **BUY / AVOID signal**  
- Probability score  
- CV metrics (Accuracy, AUC, Precision, Recall)  

---

## **12. Floating AI Chat Assistant**
Persistent, modern mini-chatbox offering:
- Risk guidelines  
- Portfolio hygiene checks  
- Basic stock insights  
- Quick technical sanity checks  

---

# 🛠️ **Tech Stack**

| Layer | Technologies |
|-------|--------------|
| Frontend | Streamlit, HTML/CSS, Plotly |
| Backend | Python, SQLite, bcrypt |
| APIs | Finnhub, yFinance |
| ML | scikit-learn, feature engineering |

---

# 📦 **Installation**

```bash
git clone <repo-url>
cd FinSight
pip install -r requirements.txt
streamlit run g.py
