import streamlit as st

# ==================== Global UI/UX CSS & Floating Chatbot Helpers ====================
# Color contrast for Selectbox/Radio and readable text in light & dark themes.
st.markdown("""
<style>
:root {
  --light-text: #0f172a;
  --light-bg: #ffffff;
  --light-surface: #f8fafc;
  --light-accent: #0ea5e9;
  --dark-text: #e5e7eb;
  --dark-bg: #0e1117;
  --dark-surface: #111827;
  --dark-accent: #22d3ee;
}
@media (prefers-color-scheme: light) {
  :root { --text-color: var(--light-text); --bg-color: var(--light-bg); --surface: var(--light-surface); --accent: var(--light-accent); }
}
@media (prefers-color-scheme: dark) {
  :root { --text-color: var(--dark-text); --bg-color: var(--dark-bg); --surface: var(--dark-surface); --accent: var(--dark-accent); }
}
html, body, .stApp { color: var(--text-color) !important; }
.stSelectbox label, .stRadio label, .stMultiSelect label { color: var(--text-color) !important; font-weight: 600; }
.stSelectbox [data-baseweb='select'] { background-color: var(--surface) !important; border-radius: 12px !important; border: 1px solid rgba(0,0,0,0.08) !important; }
.stRadio > div { background-color: var(--surface) !important; border-radius: 12px !important; padding: 8px 10px !important; border: 1px solid rgba(0,0,0,0.08) !important; }
.stButton>button, .stDownloadButton>button { border-radius: 10px !important; }
[data-baseweb='select'] [aria-hidden='true'] svg { stroke: var(--text-color) !important; }
[data-baseweb='select']:focus-within { box-shadow: 0 0 0 2px var(--accent) !important; border-color: var(--accent) !important; }
#floating-chat { position: fixed; bottom: 20px; right: 20px; width: 320px; max-height: 60vh; overflow: hidden; background: var(--surface); color: var(--text-color);
  border: 1px solid rgba(0,0,0,0.08); border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.2); z-index: 1000; }
#floating-chat .chat-header { display:flex; align-items:center; justify-content:space-between; padding:10px 12px; background: linear-gradient(135deg, var(--accent), #6ee7b7); color:white; font-weight:700; font-size:14px; }
#floating-chat .chat-body { padding:8px 10px; overflow-y:auto; max-height:40vh; background: var(--surface); }
.msg { margin:6px 0; padding:8px 10px; border-radius:10px; line-height:1.3; font-size:13px; }
.msg.user { background: rgba(14,165,233,0.15); align-self:flex-end; }
.msg.bot { background: rgba(34,211,238,0.15); }
#floating-chat .chat-footer { padding:8px 10px; font-size:12px; opacity:0.85; background: rgba(0,0,0,0.03); }

/* ===== Improved Sidebar Radio Styling ===== */
.stRadio label {
    color: var(--text-color) !important;
}
/* active radio dot */
.stRadio div[role="radio"][aria-checked="true"] svg {
    fill: #ff4b4b !important;
    stroke: #ffffff !important;
}
/* inactive radio dot */
.stRadio div[role="radio"][aria-checked="false"] svg {
    stroke: #cccccc !important;
}


/* ===== Enhanced Sidebar, Buttons & Chatbot Styling ===== */
.stRadio label, .stSelectbox label, .stMultiSelect label {
    font-weight: 600 !important;
}
@media (prefers-color-scheme: light) {
  .stRadio label, .stSelectbox label, .stMultiSelect label {
    color: #000000 !important;
  }
  .stButton>button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border-radius: 8px !important;
  }
}
@media (prefers-color-scheme: dark) {
  .stRadio label, .stSelectbox label, .stMultiSelect label {
    color: #ffffff !important;
  }
  .stButton>button {
    background-color: #3b82f6 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
  }
}

/* Compare button styling */
.compare-btn>button {
  width: 100%;
  padding: 0.6em 1em;
  border-radius: 8px;
  background: linear-gradient(90deg, #2563eb, #1d4ed8);
  color: white;
  font-weight: bold;
}
.compare-btn>button:hover {
  background: linear-gradient(90deg, #1d4ed8, #2563eb);
}

/* Chatbot modern UI */
#floating-chat {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 340px;
  max-height: 65vh;
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  font-size: 14px;
  overflow: hidden;
  z-index: 1000;
}
#floating-chat .chat-header {
  padding: 10px;
  background: linear-gradient(135deg, #2563eb, #6ee7b7);
  color: white;
  font-weight: 700;
}
#floating-chat .chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
  display: flex;
  flex-direction: column;
}
.msg {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 18px;
  margin: 4px 0;
  line-height: 1.3;
}
.msg.user {
  align-self: flex-end;
  background: #2563eb;
  color: white;
}
.msg.bot {
  align-self: flex-start;
  background: #374151;
  color: #f9fafb;
}

</style>
""", unsafe_allow_html=True)


# ---- Chatbot logic (lightweight advice engine, no external LLM) ----
import re as _re #Regular expressions
from datetime import datetime as _dt #Displays date and time
from functools import lru_cache #A decorator that caches results of a function, so if the same query is asked again, it responds faster.

@lru_cache(maxsize=128)
def _advice_for_query(q: str):
    ql = (q or '').strip().lower()
    if not ql:
        return "Ask me things like: 'Should I buy AAPL?', 'Risk on TSLA', 'Portfolio advice'."
    if any(k in ql for k in ['hello','hi','hey']):
        return "Hey there! I’m your floating AI Advisor. Ask about stocks, risk, or diversification."
    sym = None
    for token in q.split():
        if token.isalpha() and 1 < len(token) <= 5 and token.isupper():
            sym = token
            break
    if 'buy' in ql or 'invest' in ql:
        base = 'Only invest if you have a time horizon > 3 years and can tolerate drawdowns.'
        if sym: base = f'For {sym}: ' + base
        return base + ' Want me to check recent momentum and max drawdown for a quick sanity check?'
    if 'risk' in ql or 'volatility' in ql:
        return 'Rule of thumb: keep single-position risk under 5% of your portfolio and ensure sector diversification.'
    if 'diversify' in ql or 'portfolio' in ql:
        return 'Aim for a core-satellite mix: broad index funds as core, a few high-conviction satellites. Rebalance annually.'
    if sym:
        return f'{sym} noted. Consider fundamentals, recent momentum, and sector weight. Need a quick technical snapshot?'
    return 'I can discuss risk, rebalancing, and quick signals. Try: \'risk management tips\'.'
    if any(k in ql for k in ['hello','hi','hey']):
        return "Hey there! I’m your floating AI Advisor. Ask about stocks, risk, or diversification."
    sym = None
    for token in q.split():
        if token.isalpha() and 1 < len(token) <= 5 and token.isupper():
            sym = token
            break
    if 'buy' in ql or 'invest' in ql:
        base = 'Only invest if you have a time horizon > 3 years and can tolerate drawdowns.'
        if sym: base = f'For {sym}: ' + base
        return base + ' Want me to check recent momentum and max drawdown for a quick sanity check?'
    if 'risk' in ql or 'volatility' in ql:
        return 'Rule of thumb: keep single-position risk under 5% of your portfolio and ensure sector diversification.'
    if 'diversify' in ql or 'portfolio' in ql:
        return 'Aim for a core-satellite mix: broad index funds as core, a few high-conviction satellites. Rebalance annually.'
    if sym:
        return f'{sym} noted. Consider fundamentals, recent momentum, and sector weight. Need a quick technical snapshot?'
    return 'I can discuss risk, rebalancing, and quick signals. Try: \'risk management tips\'.'


def _floating_chat_ui():
    if 'floating_chat' not in st.session_state:
        st.session_state.floating_chat = [('bot', 'Hi! I’m your floating AI Advisor. Ask me about stocks or portfolio strategy.')]
    messages_html = ''
    for who, msg in st.session_state.floating_chat[-20:]:
        cls = 'bot' if who == 'bot' else 'user'
        messages_html += f'<div class="msg {cls}">{msg}</div>'
    time_str = _dt.now().strftime('%H:%M')
    panel_html = (
        '<div id="floating-chat">'
        f'<div class="chat-header">💬 AI Advisor <span>{time_str}</span></div>'
        f'<div class="chat-body">{messages_html}</div>'
        '<div class="chat-footer">Type in the bottom bar → Your message will appear here.</div>'
        '</div>'
    )
    st.markdown(panel_html, unsafe_allow_html=True)
    user_text = st.chat_input('Ask the AI Advisor…')
    if user_text:
        st.session_state.floating_chat.append(('user', user_text))
        reply = _advice_for_query(user_text)
        st.session_state.floating_chat.append(('bot', reply))

# ==================== END ADDED ====================


import yfinance as yf
import sqlite3
import pandas as pd
import numpy as np
import requests #help in making API calls
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import bcrypt
from io import BytesIO #helps in handling binary data in memory
import finnhub
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Setup sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Backend API key
FINNHUB_API_KEY = "d2g7571r01qkv5ng2ta0d2g7571r01qkv5ng2tag"

# Setup client
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)


# ===== Optional sentiment (graceful fallback) =====
try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon')
    SIA = SentimentIntensityAnalyzer()
except Exception:
    SIA = None

# ====== Email (optional) ======
import smtplib
from email.mime.text import MIMEText

def send_email(subject: str, body: str, to_email: str) -> bool:
    """Send email using Streamlit secrets (optional). Returns True on success or if not configured."""
    try:
        smtp_host = st.secrets.get("smtp_host")
        smtp_port = int(st.secrets.get("smtp_port", 587))
        smtp_user = st.secrets.get("smtp_user")
        smtp_pass = st.secrets.get("smtp_pass")
        from_email = st.secrets.get("from_email", smtp_user)
        if not smtp_host or not smtp_user or not smtp_pass:
            return False
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_email, [to_email], msg.as_string())
        return True
    except Exception:
        return False

# ---------------- STREAMLIT CONFIG ----------------
st.set_page_config(page_title="📈 FinSight", layout="wide")

# ---------------- THEME TOGGLE ----------------

if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

with st.sidebar:
    st.markdown("### 🎨 Theme")
    theme = st.radio("Choose theme", ["light", "dark"], index=0 if st.session_state["theme"]=="light" else 1)
    st.session_state["theme"] = theme

# Plotly template bound to theme
chart_template = "plotly_white" if st.session_state["theme"] == "light" else "plotly_dark"

# App-wide CSS bound to theme (avoid brittle class names; scope generic tags carefully)
if st.session_state["theme"] == "dark":
    st.markdown(
        """
        <style>
        .stApp { background-color: #0e1117; color: #fafafa; }
        .st-emotion-cache-1jicfl2 { color: #fafafa !important; }
        .stMarkdown, .stText, label, p, span, h1, h2, h3, h4, h5, h6 { color: #fafafa !important; }
        .block-container { padding-top: 1rem; }
        .metric-container { background:#161a23; border-radius:12px; padding:10px; }
        .tickerbar { color:#ffffff; background:#000000; }
        
/* ===== Improved Sidebar Radio Styling ===== */
.stRadio label {
    color: var(--text-color) !important;
}
/* active radio dot */
.stRadio div[role="radio"][aria-checked="true"] svg {
    fill: #ff4b4b !important;
    stroke: #ffffff !important;
}
/* inactive radio dot */
.stRadio div[role="radio"][aria-checked="false"] svg {
    stroke: #cccccc !important;
}


/* ===== Enhanced Sidebar, Buttons & Chatbot Styling ===== */
.stRadio label, .stSelectbox label, .stMultiSelect label {
    font-weight: 600 !important;
}
@media (prefers-color-scheme: light) {
  .stRadio label, .stSelectbox label, .stMultiSelect label {
    color: #000000 !important;
  }
  .stButton>button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border-radius: 8px !important;
  }
}
@media (prefers-color-scheme: dark) {
  .stRadio label, .stSelectbox label, .stMultiSelect label {
    color: #ffffff !important;
  }
  .stButton>button {
    background-color: #3b82f6 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
  }
}

/* Compare button styling */
.compare-btn>button {
  width: 100%;
  padding: 0.6em 1em;
  border-radius: 8px;
  background: linear-gradient(90deg, #2563eb, #1d4ed8);
  color: white;
  font-weight: bold;
}
.compare-btn>button:hover {
  background: linear-gradient(90deg, #1d4ed8, #2563eb);
}

/* Chatbot modern UI */
#floating-chat {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 340px;
  max-height: 65vh;
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  font-size: 14px;
  overflow: hidden;
  z-index: 1000;
}
#floating-chat .chat-header {
  padding: 10px;
  background: linear-gradient(135deg, #2563eb, #6ee7b7);
  color: white;
  font-weight: 700;
}
#floating-chat .chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
  display: flex;
  flex-direction: column;
}
.msg {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 18px;
  margin: 4px 0;
  line-height: 1.3;
}
.msg.user {
  align-self: flex-end;
  background: #2563eb;
  color: white;
}
.msg.bot {
  align-self: flex-start;
  background: #374151;
  color: #f9fafb;
}

</style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .stApp { background-color: #ffffff; color: #0e1117; }
        .st-emotion-cache-1jicfl2 { color: #0e1117 !important; }
        .stMarkdown, .stText, label, p, span, h1, h2, h3, h4, h5, h6 { color: #0e1117 !important; }
        .block-container { padding-top: 1rem; }
        .metric-container { background:#f5f6f7; border-radius:12px; padding:10px; }
        .tickerbar { color:#0e1117; background:#f0f0f0; }
        
/* ===== Improved Sidebar Radio Styling ===== */
.stRadio label {
    color: var(--text-color) !important;
}
/* active radio dot */
.stRadio div[role="radio"][aria-checked="true"] svg {
    fill: #ff4b4b !important;
    stroke: #ffffff !important;
}
/* inactive radio dot */
.stRadio div[role="radio"][aria-checked="false"] svg {
    stroke: #cccccc !important;
}


/* ===== Enhanced Sidebar, Buttons & Chatbot Styling ===== */
.stRadio label, .stSelectbox label, .stMultiSelect label {
    font-weight: 600 !important;
}
@media (prefers-color-scheme: light) {
  .stRadio label, .stSelectbox label, .stMultiSelect label {
    color: #000000 !important;
  }
  .stButton>button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border-radius: 8px !important;
  }
}
@media (prefers-color-scheme: dark) {
  .stRadio label, .stSelectbox label, .stMultiSelect label {
    color: #ffffff !important;
  }
  .stButton>button {
    background-color: #3b82f6 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
  }
}

/* Compare button styling */
.compare-btn>button {
  width: 100%;
  padding: 0.6em 1em;
  border-radius: 8px;
  background: linear-gradient(90deg, #2563eb, #1d4ed8);
  color: white;
  font-weight: bold;
}
.compare-btn>button:hover {
  background: linear-gradient(90deg, #1d4ed8, #2563eb);
}

/* Chatbot modern UI */
#floating-chat {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 340px;
  max-height: 65vh;
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  font-size: 14px;
  overflow: hidden;
  z-index: 1000;
}
#floating-chat .chat-header {
  padding: 10px;
  background: linear-gradient(135deg, #2563eb, #6ee7b7);
  color: white;
  font-weight: 700;
}
#floating-chat .chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
  display: flex;
  flex-direction: column;
}
.msg {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 18px;
  margin: 4px 0;
  line-height: 1.3;
}
.msg.user {
  align-self: flex-end;
  background: #2563eb;
  color: white;
}
.msg.bot {
  align-self: flex-start;
  background: #374151;
  color: #f9fafb;
}

</style>
        """,
        unsafe_allow_html=True
    )

# ---------------- USER DB SETUP ----------------
user_conn = sqlite3.connect("users.db", check_same_thread=False)
user_c = user_conn.cursor()
user_c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                password BLOB
            )''')
user_conn.commit()

# ---------------- PORTFOLIO DB (multi-portfolio) ----------------
conn = sqlite3.connect("portfolio.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS portfolios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    name TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS holdings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER,
    ticker TEXT,
    shares REAL,
    buy_price REAL,
    FOREIGN KEY(portfolio_id) REFERENCES portfolios(id)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    ticker TEXT,
    pct_move REAL,
    direction TEXT CHECK(direction IN ('up','down','any')) DEFAULT 'any',
    email_notify INTEGER DEFAULT 0
)
""")
conn.commit()

# ---------------- STATIC DATA ----------------
available_stocks = {
    "AAPL": 180.0, "TSLA": 250.0, "MSFT": 330.0, "GOOGL": 135.0, "AMZN": 140.0,
    "META": 310.0, "NVDA": 450.0, "NFLX": 420.0, "AMD": 110.0, "INTC": 35.0,
    "ORCL": 115.0, "IBM": 145.0, "PYPL": 65.0, "ADBE": 520.0, "CRM": 210.0,
    "UBER": 48.0, "LYFT": 12.0, "BA": 220.0, "DIS": 95.0, "NKE": 105.0,
    "WMT": 160.0, "COST": 560.0, "JPM": 150.0, "GS": 340.0, "V": 245.0
}

# Sector map (fallback if yfinance info is missing)
sector_map = {
    "AAPL":"Technology","TSLA":"Consumer Discretionary","MSFT":"Technology","GOOGL":"Communication Services",
    "AMZN":"Consumer Discretionary","META":"Communication Services","NVDA":"Technology","NFLX":"Communication Services",
    "AMD":"Technology","INTC":"Technology","ORCL":"Technology","IBM":"Technology","PYPL":"Financials",
    "ADBE":"Technology","CRM":"Technology","UBER":"Industrials","LYFT":"Industrials","BA":"Industrials",
    "DIS":"Communication Services","NKE":"Consumer Discretionary","WMT":"Consumer Staples","COST":"Consumer Staples",
    "JPM":"Financials","GS":"Financials","V":"Financials"
}

# Crypto universe (extendable)
crypto_universe = ["BTC-USD","ETH-USD","SOL-USD","XRP-USD"]

# ---------------- AUTH HELPERS ----------------

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    except Exception:
        return False


def add_user(name, email, password):
    try:
        user_c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                  (name, email, hash_password(password)))
        user_conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def get_user(email):
    user_c.execute("SELECT * FROM users WHERE email = ?", (email,))
    return user_c.fetchone()


def update_password(email, new_password):
    user_c.execute("UPDATE users SET password = ? WHERE email = ?",
              (hash_password(new_password), email))
    user_conn.commit()

# ---------------- SESSION STATE ----------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None

# ---------------- CACHING HELPERS ----------------
@st.cache_data(ttl=120)
def get_bulk_prices(tickers):
    result = {}
    if not tickers:
        return result
    try:
        data = yf.download(tickers=" ".join(tickers), period="2d", group_by="ticker", auto_adjust=False, progress=False)
        if isinstance(data.columns, pd.MultiIndex):
            for t in tickers:
                try:
                    closes = data[(t, "Close")].dropna()
                    if len(closes) >= 2:
                        result[t] = (float(closes.iloc[-1]), float(closes.iloc[-2]))
                    elif len(closes) == 1:
                        result[t] = (float(closes.iloc[-1]), None)
                except Exception:
                    result[t] = (None, None)
        else:
            closes = data["Close"].dropna()
            t = tickers[0]
            if len(closes) >= 2:
                result[t] = (float(closes.iloc[-1]), float(closes.iloc[-2]))
            elif len(closes) == 1:
                result[t] = (float(closes.iloc[-1]), None)
    except Exception:
        for t in tickers:
            try:
                hist = yf.Ticker(t).history(period="2d")
                if len(hist) >= 2:
                    result[t] = (float(hist["Close"].iloc[-1]), float(hist["Close"].iloc[-2]))
                elif len(hist) == 1:
                    result[t] = (float(hist["Close"].iloc[-1]), None)
                else:
                    result[t] = (None, None)
            except Exception:
                result[t] = (None, None)
    return result

@st.cache_data(ttl=1800)
def get_news_data(symbol="AAPL"):
    try:
        # Fetch company news from the past 7 days
        from datetime import date, timedelta
        today = date.today()
        last_week = today - timedelta(days=7)
        news = finnhub_client.company_news(symbol, _from=str(last_week), to=str(today))
        return news
    except Exception as e:
        return [{"headline": f"Error fetching news: {e}"}]


@st.cache_data(ttl=600)
def download_history(tickers, period="1y"):
    df = yf.download(tickers=tickers, period=period, auto_adjust=False, group_by="ticker", progress=False)
    return df

# ---------------- PORTFOLIO HELPERS ----------------

def ensure_default_portfolio(user_email: str) -> int:
    c.execute("SELECT id FROM portfolios WHERE user_email=? ORDER BY id LIMIT 1", (user_email,))
    row = c.fetchone()
    if row:
        return row[0]
    c.execute("INSERT INTO portfolios (user_email, name) VALUES (?, ?)", (user_email, "Main"))
    conn.commit()
    return c.lastrowid


def list_portfolios(user_email: str) -> pd.DataFrame:
    c.execute("SELECT id, name FROM portfolios WHERE user_email=?", (user_email,))
    rows = c.fetchall()
    return pd.DataFrame(rows, columns=["id","name"]) if rows else pd.DataFrame(columns=["id","name"])


def add_portfolio(user_email: str, name: str):
    c.execute("INSERT INTO portfolios (user_email, name) VALUES (?, ?)", (user_email, name))
    conn.commit()


def add_stock(portfolio_id, ticker, shares, buy_price):
    c.execute("INSERT INTO holdings (portfolio_id, ticker, shares, buy_price) VALUES (?, ?, ?, ?)",
              (portfolio_id, ticker.upper(), shares, buy_price))
    conn.commit()


def remove_stock(portfolio_id, ticker):
    c.execute("DELETE FROM holdings WHERE portfolio_id=? AND ticker=?", (portfolio_id, ticker.upper()))
    conn.commit()


def get_portfolio_holdings(portfolio_id) -> pd.DataFrame:
    c.execute("SELECT ticker, shares, buy_price FROM holdings WHERE portfolio_id=?", (portfolio_id,))
    rows = c.fetchall()
    return pd.DataFrame(rows, columns=["Ticker","Shares","Buy Price"]) if rows else pd.DataFrame(columns=["Ticker","Shares","Buy Price"])

# ===== Risk metrics =====

def compute_portfolio_timeseries(holdings_df: pd.DataFrame, period="1y"):
    if holdings_df.empty:
        return None, None
    tickers = holdings_df["Ticker"].tolist()
    hist = yf.download(tickers=tickers, period=period, auto_adjust=False, group_by="ticker", progress=False)

    # Build wide close prices
    closes = pd.DataFrame()
    if isinstance(hist.columns, pd.MultiIndex):
        for t in tickers:
            try:
                closes[t] = hist[(t, "Close")]
            except Exception:
                pass
    else:
        closes[tickers[0]] = hist["Close"]
    closes = closes.dropna(how='all')

    # Market values per day
    quantities = holdings_df.set_index("Ticker")["Shares"]
    for t in closes.columns:
        closes[t] = closes[t].astype(float)
    portfolio_value = (closes * quantities).sum(axis=1)

    # Daily returns
    port_ret = portfolio_value.pct_change().dropna()
    return portfolio_value, port_ret


def sharpe_ratio(returns: pd.Series, risk_free_annual=0.02):
    if returns is None or returns.empty:
        return None
    mean_daily = returns.mean()
    std_daily = returns.std()
    if std_daily == 0 or np.isnan(std_daily):
        return None
    trading_days = 252
    rf_daily = (1 + risk_free_annual) ** (1/trading_days) - 1
    sharpe = (mean_daily - rf_daily) / std_daily * np.sqrt(trading_days)
    return float(sharpe)


def portfolio_beta(port_returns: pd.Series, bench_returns: pd.Series):
    if port_returns is None or port_returns.empty or bench_returns is None or bench_returns.empty:
        return None
    aligned = pd.concat([port_returns, bench_returns], axis=1).dropna()
    if aligned.shape[0] < 5:
        return None
    cov = np.cov(aligned.iloc[:,0], aligned.iloc[:,1])[0,1]
    var = np.var(aligned.iloc[:,1])
    if var == 0:
        return None
    return float(cov/var)


# ====== ML ADVISOR (5y training, invest/not) ======
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler

@st.cache_data(ttl=3600)
def _download_5y(tickers: list[str]) -> dict[str, pd.DataFrame]:
    out = {}
    if not tickers:
        return out
    try:
        data = yf.download(" ".join(tickers), period="5y", auto_adjust=False, group_by="ticker", progress=False)
        multi = isinstance(data.columns, pd.MultiIndex)
        for t in tickers:
            try:
                if multi:
                    df = data[t].dropna().copy()
                else:
                    df = data.copy()
                df = df[["Open","High","Low","Close","Volume"]].dropna()
                out[t] = df
            except Exception:
                pass
    except Exception:
        pass
    for t in tickers:
        if t not in out:
            try:
                out[t] = yf.Ticker(t).history(period="5y")[["Open","High","Low","Close","Volume"]].dropna()
            except Exception:
                out[t] = pd.DataFrame()
    return out

def _rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    avg_gain = up.rolling(period).mean()
    avg_loss = down.rolling(period).mean()
    rs = avg_gain / (avg_loss.replace(0, np.nan))
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)

def _build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ret1"] = out["Close"].pct_change()
    out["ret5"] = out["Close"].pct_change(5)
    out["ret20"] = out["Close"].pct_change(20)
    out["vol20"] = out["ret1"].rolling(20).std()
    out["sma5"] = out["Close"].rolling(5).mean()
    out["sma20"] = out["Close"].rolling(20).mean()
    out["sma_ratio"] = out["sma5"] / out["sma20"]
    out["rsi14"] = _rsi(out["Close"], 14)
    ema12 = out["Close"].ewm(span=12, adjust=False).mean()
    ema26 = out["Close"].ewm(span=26, adjust=False).mean()
    out["macd"] = ema12 - ema26
    out["macd_signal"] = out["macd"].ewm(span=9, adjust=False).mean()
    out = out.dropna()
    return out

def _make_labeled_dataset(prices: dict[str, pd.DataFrame], horizon_days: int = 20, target_threshold: float = 0.05) -> tuple[pd.DataFrame, pd.Series]:
    rows = []
    for t, df in prices.items():
        if df is None or df.empty:
            continue
        feat = _build_features(df)
        future = df["Close"].shift(-horizon_days) / df["Close"] - 1.0
        y = (future > target_threshold).astype(int)
        aligned = feat.join(y.rename("target")).dropna()
        if aligned.empty:
            continue
        aligned["Ticker"] = t
        rows.append(aligned)
    if not rows:
        return pd.DataFrame(), pd.Series(dtype=int)
    big = pd.concat(rows, axis=0)
    X = big[["ret1","ret5","ret20","vol20","sma_ratio","rsi14","macd","macd_signal","Volume"]].copy()
    y = big["target"].astype(int)
    scaler = StandardScaler()
    X[["ret1","ret5","ret20","vol20","rsi14","macd","macd_signal"]] = scaler.fit_transform(
        X[["ret1","ret5","ret20","vol20","rsi14","macd","macd_signal"]]
    )
    return X, y

@st.cache_resource(show_spinner=False)
def train_ml_model(tickers: list[str], horizon_days: int = 20, target_threshold: float = 0.05, n_splits: int = 5):
    prices = _download_5y(tickers)
    X, y = _make_labeled_dataset(prices, horizon_days, target_threshold)
    if X.empty or y.empty:
        return None, {}, prices

    tscv = TimeSeriesSplit(n_splits=n_splits)
    model = RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=42, n_jobs=-1)

    accs, aucs, precs, recs = [], [], [], []
    for train_idx, valid_idx in tscv.split(X):
        model.fit(X.iloc[train_idx], y.iloc[train_idx])
        proba = model.predict_proba(X.iloc[valid_idx])[:, 1]
        pred = (proba >= 0.5).astype(int)
        accs.append(accuracy_score(y.iloc[valid_idx], pred))
        try:
            aucs.append(roc_auc_score(y.iloc[valid_idx], proba))
        except ValueError:
            aucs.append(np.nan)
        precs.append(precision_score(y.iloc[valid_idx], pred, zero_division=0))
        recs.append(recall_score(y.iloc[valid_idx], pred, zero_division=0))

    model.fit(X, y)
    metrics = {
        "accuracy": float(np.nanmean(accs)),
        "roc_auc": float(np.nanmean(aucs)),
        "precision": float(np.nanmean(precs)),
        "recall": float(np.nanmean(recs)),
        "samples": int(len(y))
    }
    return model, metrics, prices

def predict_signal(model, latest_df: pd.DataFrame, horizon_days: int = 20, threshold_prob: float = 0.5):
    if model is None or latest_df is None or latest_df.empty:
        return None
    feat = _build_features(latest_df).iloc[-1:]
    X = feat[["ret1","ret5","ret20","vol20","sma_ratio","rsi14","macd","macd_signal","Volume"]].copy()
    scaler = StandardScaler()
    X[["ret1","ret5","ret20","vol20","rsi14","macd","macd_signal"]] = scaler.fit_transform(
        X[["ret1","ret5","ret20","vol20","rsi14","macd","macd_signal"]]
    )
    prob = float(model.predict_proba(X)[:, 1][0])
    label = "✅ BUY" if prob >= threshold_prob else "🚫 AVOID"
    return {"prob": prob, "label": label}

# ====== UI START ======

if not st.session_state["authenticated"]:
    st.title("🔐 Welcome to FinSight")

    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Forgot Password"])

    with tab1:
        st.subheader("🔑 Existing User Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            user = get_user(email)
            if user and verify_password(password, user[3]):
                st.success(f"✅ Welcome {user[1]}!")
                st.session_state["authenticated"] = True
                st.session_state["user"] = user
                st.rerun()
            else:
                st.error("❌ Invalid email or password")

    with tab2:
        st.subheader("📝 Create New Account")
        name = st.text_input("Full Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_cpass")
        if st.button("Register"):
            if password != confirm_password:
                st.error("❌ Passwords do not match")
            elif add_user(name, email, password):
                st.success("✅ Account created! Please login.")
            else:
                st.error("❌ Email already registered")

    with tab3:
        st.subheader("🔄 Reset Password")
        email = st.text_input("Registered email", key="reset_email")
        new_password = st.text_input("New Password", type="password", key="reset_pass")
        confirm_new_password = st.text_input("Confirm New Password", type="password", key="reset_cpass")
        if st.button("Reset Password"):
            user = get_user(email)
            if not user:
                st.error("❌ Email not found")
            elif new_password != confirm_new_password:
                st.error("❌ Passwords do not match")
            else:
                update_password(email, new_password)
                st.success("✅ Password updated! Please login.")

else:
    # ----- Authenticated area -----
    user = st.session_state["user"]
    name = user[1]
    email = user[2]

    st.title(f"💹 Stock Portfolio Pro — Hello, {name}!")

   # ----------------- FLOATING TICKER BAR (ALL 25 STOCKS) -----------------
# Make sure available_stocks dict has your 25 stock tickers
all_symbols = list(available_stocks.keys())   # use all 25, not just selected
price_map = get_bulk_prices(all_symbols)

perf_snippets = []
for sym in all_symbols:
    last, prev = price_map.get(sym, (None, None))
    if last is None:
        continue
    if prev is not None and prev != 0:
        change = last - prev
        pct = (change / prev) * 100
    else:
        change, pct = 0.0, 0.0

    # Background + animation
    if change > 0:
        bg = "#37d67a"  # green
        anim = "pulse-up"
    elif change < 0:
        bg = "#ff4d4f"  # red
        anim = "pulse-down"
    else:
        bg = "#999"     # neutral gray
        anim = ""

    perf_snippets.append(
        f"<span class='{anim}' style='background:{bg}; color:white; font-weight:600; "
        f"padding:4px 10px; margin-right:10px; border-radius:6px;'>"
        f"{sym}: {last:.2f} ({pct:+.2f}%)</span>"
    )

# CSS styles (UPDATED: smoother, reliable scrolling without changing HTML structure)
st.markdown(
    """
    <style>
    .tickerbar {
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        font-size:18px; 
        font-weight:600; 
        border-radius:8px; 
        padding:12px;
        margin-bottom: 12px;
        color: #ffffff;
        background: linear-gradient(90deg, #0f172a, #1e293b, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 25s ease infinite;
        box-sizing: border-box;
    }
    .tickerbar span {
        display: inline-block;
        margin-right: 20px;
        animation: scrollTicker 40s linear infinite;
    }
    @keyframes scrollTicker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    @keyframes gradientBG { 
        0% {background-position:0% 50%;} 
        50%{background-position:100% 50%;} 
        100%{background-position:0% 50%;} 
    }
    @keyframes pulse-up { 
        0% {box-shadow:0 0 0 0 rgba(34,197,94,0.7);} 
        70% {box-shadow:0 0 0 12px rgba(34,197,94,0);} 
        100% {box-shadow:0 0 0 0 rgba(34,197,94,0);} 
    }
    @keyframes pulse-down { 
        0% {box-shadow:0 0 0 0 rgba(239,68,68,0.7);} 
        70% {box-shadow:0 0 0 12px rgba(239,68,68,0);} 
        100% {box-shadow:0 0 0 0 rgba(239,68,68,0);} 
    }
    .pulse-up { animation: pulse-up 2s infinite; }
    .pulse-down { animation: pulse-down 2s infinite; }
    </style>
    """,
    unsafe_allow_html=True
)

class render_chatbot_section:
    def __init__(self):
        pass

# Render ticker bar
if perf_snippets:
    ticker_html = "".join(perf_snippets)
    st.markdown(f"<div class='tickerbar'>{ticker_html}</div>", unsafe_allow_html=True)



    # Sidebar Navigation
    menu = st.sidebar.radio(
        "📌 Navigation",
        [
            "Dashboard", "Add Stock", "Remove Stock", "Alerts", "Watchlist",
            "Portfolio Value", "Risk & Correlation", "Sectors & Allocation",
            "Benchmark Compare", "Crypto", "News", "Export/Reports", "AI Advisor", "Logout"
        ]
    )

    # Portfolio picker
    with st.sidebar:
        st.markdown("---")
        st.subheader("📁 Portfolios")
        portfolios_df = list_portfolios(email)
        if portfolios_df.empty:
            default_id = ensure_default_portfolio(email)
            portfolios_df = list_portfolios(email)
        portfolio_names = portfolios_df["name"].tolist()
        portfolio_ids = portfolios_df["id"].tolist()
        idx = st.selectbox("Select portfolio", range(len(portfolio_names)), format_func=lambda i: portfolio_names[i])
        current_portfolio_id = int(portfolio_ids[idx]) if len(portfolio_ids)>0 else ensure_default_portfolio(email)
        new_port_name = st.text_input("New portfolio name")
        if st.button("➕ Create portfolio") and new_port_name.strip():
            add_portfolio(email, new_port_name.strip())
            st.rerun()

    # ---- Helper to fetch current holdings ----
    def current_holdings_df():
        return get_portfolio_holdings(current_portfolio_id)

    # ---------------- DASHBOARD ----------------
    if menu == "Dashboard":
        st.header("📊 Your Portfolio Overview")

        df = current_holdings_df()
        if df.empty:
            st.info("⚠️ No stocks in portfolio. Add some from the sidebar!")
        else:
            # Add current price, value, PnL
            last_prices = {}
            for t in df["Ticker"].tolist():
                try:
                    p = yf.Ticker(t).history(period="1d")["Close"].iloc[-1]
                except Exception:
                    p = np.nan
                last_prices[t] = p
            df["Current Price"] = df["Ticker"].map(last_prices)
            df["Value"] = df["Shares"] * df["Current Price"].astype(float)
            df["PnL"] = df["Shares"] * (df["Current Price"].astype(float) - df["Buy Price"].astype(float))
            st.dataframe(df, use_container_width=True)

            # Trends
            st.subheader("📈 Stock Trends (Last 6 Months)")
            for ticker in df["Ticker"]:
                hist = yf.Ticker(ticker).history(period="6mo")
                if not hist.empty:
                    fig = px.line(hist, x=hist.index, y="Close", title=f"{ticker} Trend", template=chart_template)
                    st.plotly_chart(fig, use_container_width=True)

            # Profit/Loss pies
            st.subheader("📊 Profit vs Loss Distribution")
            col1, col2 = st.columns(2)
            profit_df = df[df["PnL"] > 0]
            loss_df = df[df["PnL"] < 0]
            with col1:
                st.markdown("### ✅ Profitable Stocks")
                if not profit_df.empty:
                    profit_fig = px.pie(profit_df, names="Ticker", values="PnL",
                                        color="Ticker", title="PnL from Profitable Stocks", template=chart_template)
                    st.plotly_chart(profit_fig, use_container_width=True)
                else:
                    st.info("No profitable stocks yet.")
            with col2:
                st.markdown("### ❌ Losing Stocks")
                if not loss_df.empty:
                    loss_fig = px.pie(loss_df, names="Ticker", values="PnL",
                                      color="Ticker", title="PnL from Losing Stocks", template=chart_template)
                    st.plotly_chart(loss_fig, use_container_width=True)
                else:
                    st.info("No losing stocks yet.")

    # ---------------- ADD STOCK ----------------
    elif menu == "Add Stock":
        st.header("➕ Add a Stock")
        ticker = st.selectbox("Select Stock", list(available_stocks.keys()))
        shares = st.number_input("Shares", min_value=1, step=1)
        buy_price = st.number_input("Buy Price (USD)", min_value=0.0, step=0.01, value=float(available_stocks[ticker]))
        if st.button("Add Stock"):
            add_stock(current_portfolio_id, ticker, shares, buy_price)
            st.success(f"✅ {shares} shares of {ticker} added to '{portfolio_names[idx]}'!")

    # ---------------- REMOVE STOCK ----------------
    elif menu == "Remove Stock":
        st.header("❌ Remove Stock")
        port_df = current_holdings_df()
        if port_df.empty:
            st.info("⚠️ No stocks in this portfolio.")
        else:
            selected = st.selectbox("Select stock", port_df["Ticker"].tolist())
            if st.button("Remove"):
                remove_stock(current_portfolio_id, selected)
                st.warning(f"{selected} removed!")

    # ---------------- ALERTS ----------------
    elif menu == "Alerts":
        st.header("🔔 Price Move Alerts")
        st.write("Create alerts for intraday % moves relative to previous close.")
        ticker = st.selectbox("Ticker", list(available_stocks.keys()))
        pct_move = st.slider("% move threshold", 1.0, 20.0, 5.0, step=0.5)
        direction = st.selectbox("Direction", ["up","down","any"])
        email_notify = st.checkbox("Send email when triggered (requires SMTP secrets)")
        if st.button("Save alert"):
            c.execute("INSERT INTO alerts (user_email, ticker, pct_move, direction, email_notify) VALUES (?,?,?,?,?)",
                      (email, ticker, pct_move, direction, 1 if email_notify else 0))
            conn.commit()
            st.success("✅ Alert saved")

        st.subheader("Your alerts")
        c.execute("SELECT id, ticker, pct_move, direction, email_notify FROM alerts WHERE user_email=?", (email,))
        rows = c.fetchall()
        if rows:
            alert_df = pd.DataFrame(rows, columns=["id","ticker","pct_move","direction","email_notify"])
            st.dataframe(alert_df.drop(columns=["id"]))
        else:
            st.info("No alerts yet.")

        st.subheader("Triggered (now)")
        if rows:
            tickers_to_check = list(set([r[1] for r in rows]))
            prices = get_bulk_prices(tickers_to_check)
            for aid, t, thr, direc, em in rows:
                last, prev = prices.get(t, (None, None))
                if last is None or prev is None or prev==0:
                    continue
                pct = (last - prev)/prev*100
                trig = (direc=="any" and abs(pct)>=thr) or (direc=="up" and pct>=thr) or (direc=="down" and pct<=-thr)
                if trig:
                    st.warning(f"⚠️ {t} moved {pct:+.2f}% (threshold {thr}%)")

                    # === EMAIL NOTIFICATION FOR PRICE MOVE ALERTS (uses checkbox) ===
                    if em:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                        sign = "up" if pct >= 0 else "down"
                        subject = f"Alert: {t} moved {pct:+.2f}% ({sign}, threshold {thr}%)"
                        body = (
                            f"Hello {name},\n\n"
                            f"Your price alert has triggered.\n\n"
                            f"Ticker: {t}\n"
                            f"Move: {pct:+.2f}% ({sign})\n"
                            f"Threshold: {thr:.2f}%  Direction: {direc}\n"
                            f"Last Price: {last:.2f}\nPrevious Close: {prev:.2f}\n"
                            f"Time: {timestamp}\n\n"
                            f"- FinSight"
                        )
                        sent = send_email(subject=subject, body=body, to_email=email)
                        if sent:
                            st.success("📧 Email sent ✅")
                        else:
                            st.caption("Email not sent (SMTP not configured).")

    # ---------------- WATCHLIST ----------------
    elif menu == "Watchlist":
        st.header("👀 Watchlist with Live Trends")
        selected_stocks = st.multiselect("Select stocks to watch", list(available_stocks.keys()), default=["AAPL","TSLA","MSFT"])
        def get_stock_data(symbol):
            stock = yf.Ticker(symbol)
            hist = stock.history(period="6mo")
            latest_price = hist["Close"].iloc[-1] if not hist.empty else None
            prev_price = hist["Close"].iloc[-2] if len(hist) > 1 else None
            change_pct = ((latest_price - prev_price) / prev_price) * 100 if prev_price else 0
            return hist, latest_price, change_pct
        for symbol in selected_stocks:
            hist, price, change_pct = get_stock_data(symbol)
            col1, col2, col3, col4 = st.columns([1,1,1,3])
            col1.markdown(f"**{symbol}**")
            col2.write(f"${price:.2f}" if price else "N/A")
            col3.write(f"{change_pct:+.2f}%")
            sparkline = go.Figure()
            sparkline.add_trace(go.Scatter(y=hist["Close"], mode="lines"))
            sparkline.update_layout(height=60, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False), template=chart_template)
            col4.plotly_chart(sparkline, use_container_width=True)
        if selected_stocks:
            selected_stock = st.selectbox("🔍 Detailed view:", selected_stocks)
            hist = yf.Ticker(selected_stock).history(period="1y")
            st.markdown(f"### 📈 {selected_stock} Detailed Chart")
            fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.update_layout(xaxis_rangeslider_visible=False, height=500, template=chart_template)
            st.plotly_chart(fig, use_container_width=True)

    # ---------------- PORTFOLIO VALUE (timeline + benchmark) ----------------
    elif menu == "Portfolio Value":
        st.header("💼 Portfolio Value Over Time")
        period = st.selectbox("Period", ["6mo","1y","2y"], index=1)
        holdings = current_holdings_df()
        if holdings.empty:
            st.info("Add holdings to see timeline.")
        else:
            port_val, port_ret = compute_portfolio_timeseries(holdings, period=period)
            if port_val is not None:
                fig = px.line(port_val, title="Portfolio total value", labels={"value":"USD","index":"Date"}, template=chart_template)
                st.plotly_chart(fig, use_container_width=True)
            
            # Compare to benchmark
            bench = st.selectbox("Benchmark", ["^GSPC (S&P 500)", "^NSEI (NIFTY 50)", "^BSESN (Sensex)"])
            bench_ticker = bench.split(" ")[0]
            bh = yf.download(bench_ticker, period=period, progress=False)["Close"].dropna()

            if port_val is not None and not bh.empty:
                # Ensure both are Series
                if isinstance(bh, pd.DataFrame):
                    bh = bh.iloc[:, 0]
                bh = bh.rename("Benchmark")

                if isinstance(port_val, pd.DataFrame):
                    port_val = port_val.iloc[:, 0]
                port_val = port_val.rename("Portfolio")

                aligned = pd.concat([port_val, bh], axis=1).dropna()

                # Normalize both to 100 at start
                norm = aligned / aligned.iloc[0] * 100

                fig2 = px.line(norm, title="Indexed Performance (100 = start)", template=chart_template)
                st.plotly_chart(fig2, use_container_width=True)

    # ---------------- RISK & CORRELATION ----------------
    elif menu == "Risk & Correlation":
        st.header("📉 Risk Metrics & Correlation")
        period = st.selectbox("Period", ["6mo","1y","2y"], index=1)
        holdings = current_holdings_df()
        if holdings.empty:
            st.info("Add holdings to see risk metrics.")
        else:
            port_val, port_ret = compute_portfolio_timeseries(holdings, period=period)
            bench_ticker = st.selectbox("Beta vs.", ["^GSPC","^NSEI","^BSESN"], index=0)
            bench = yf.download(bench_ticker, period=period, progress=False)["Close"].pct_change().dropna()
            sr = sharpe_ratio(port_ret)
            beta = portfolio_beta(port_ret, bench)
            vol_annual = (port_ret.std() * np.sqrt(252)) if port_ret is not None else None
            col1, col2, col3 = st.columns(3)
            col1.metric("Sharpe (rf≈2%)", f"{sr:.2f}" if sr is not None else "N/A")
            col2.metric("Beta", f"{beta:.2f}" if beta is not None else "N/A")
            col3.metric("Volatility (ann.)", f"{vol_annual*100:.2f}%" if vol_annual is not None else "N/A")

            # Correlation heatmap
            tickers = holdings["Ticker"].tolist()
            hist = yf.download(tickers=tickers, period=period, progress=False, group_by="ticker")
            closes = pd.DataFrame()
            if isinstance(hist.columns, pd.MultiIndex):
                for t in tickers:
                    try:
                        closes[t] = hist[(t, "Close")]
                    except Exception:
                        pass
            else:
                closes[tickers[0]] = hist["Close"]
            rets = closes.pct_change().dropna(how='all')
            corr = rets.corr().fillna(0)
            heat = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Heatmap", template=chart_template)
            st.plotly_chart(heat, use_container_width=True)

    # ---------------- SECTORS & ALLOCATION ----------------
    elif menu == "Sectors & Allocation":
        st.header("🏷️ Sector Allocation & Concentration")
        holdings = current_holdings_df()
        if holdings.empty:
            st.info("Add holdings to see allocation.")
        else:
            prices = {t: yf.Ticker(t).history(period="1d")["Close"].iloc[-1] for t in holdings["Ticker"]}
            holdings["Value"] = holdings.apply(lambda r: r["Shares"] * prices.get(r["Ticker"], np.nan), axis=1)
            # Try to fetch sector via yfinance; fallback to sector_map
            sectors = {}
            for t in holdings["Ticker"]:
                sec = None
                try:
                    info = yf.Ticker(t).get_info()
                    sec = info.get("sector") if isinstance(info, dict) else None
                except Exception:
                    sec = None
                sectors[t] = sec or sector_map.get(t, "Unknown")
            holdings["Sector"] = holdings["Ticker"].map(sectors)
            sec_df = holdings.groupby("Sector", as_index=False)["Value"].sum().sort_values("Value", ascending=False)
            pie = px.pie(sec_df, names="Sector", values="Value", title="Sector Allocation", template=chart_template)
            st.plotly_chart(pie, use_container_width=True)
            # Concentration (treemap by ticker)
            tree = px.treemap(holdings, path=["Sector","Ticker"], values="Value", title="Holdings Treemap", template=chart_template)
            st.plotly_chart(tree, use_container_width=True)
            # Concentration risk warning
            if not sec_df.empty and (sec_df.iloc[0]['Value'] / sec_df['Value'].sum()) > 0.6:
                st.warning("🚨 High concentration risk: Top sector > 60% of portfolio")

    # ---------------- BENCHMARK COMPARE ----------------
    elif menu == "Benchmark Compare":
        st.header("⚖️ Compare Individual Stocks vs Benchmark")
        tickers = st.multiselect("Select tickers", list(available_stocks.keys()), default=["AAPL","MSFT","NVDA"])
        bench = st.selectbox("Benchmark", ["^GSPC (S&P 500)", "^NSEI (NIFTY 50)", "^BSESN (Sensex)"])
        period = st.selectbox("Period", ["6mo","1y","2y"], index=1)
        if tickers:
            bench_ticker = bench.split(" ")[0]
            data = yf.download(tickers + [bench_ticker], period=period, group_by="ticker", progress=False)
            close = {}
            for t in tickers:
                try:
                    close[t] = data[(t, 'Close')]
                except Exception:
                    pass
            try:
                close['Benchmark'] = data[(bench_ticker, 'Close')]
            except Exception:
                close['Benchmark'] = yf.download(bench_ticker, period=period, progress=False)['Close']
            df = pd.DataFrame(close).dropna(how='all')
            norm = df / df.iloc[0] * 100
            fig = px.line(norm, title="Indexed to 100 at start", template=chart_template)
            st.plotly_chart(fig, use_container_width=True)

    # ---------------- CRYPTO (enhanced) ----------------
    elif menu == "Crypto":
        st.header("🪙 Crypto Watch — Prices, Returns & Mini-Analytics")
        coins = st.multiselect("Select coins", crypto_universe, default=["BTC-USD","ETH-USD"]) 
        lookback = st.selectbox("Lookback", ["1mo","3mo","6mo","1y"], index=2)

        if coins:
            data = yf.download(tickers=coins, period=lookback, group_by="ticker", progress=False)
            metrics_rows = []

            for coin in coins:
                # ---- Ensure we always get a Series ----
                try:
                    if isinstance(data, pd.DataFrame) and (coin, "Close") in data.columns:
                        close = data[(coin, "Close")]
                    else:
                        close = yf.download(coin, period=lookback, progress=False)["Close"]
                except Exception:
                    continue

                if close is None or close.empty:
                    continue

                # Calculate metrics
                last_price = float(close.iloc[-1])
                ret_pct = float((close.iloc[-1] / close.iloc[0] - 1) * 100) if len(close) > 1 else 0.0
                vol_annual = float(close.pct_change().std() * np.sqrt(252) * 100)

                metrics_rows.append([coin, last_price, ret_pct, vol_annual])

                # ---- Safe plotting ----
                close = close.dropna()

                # If DataFrame has multi-index columns, flatten
                if isinstance(close, pd.DataFrame):
                    close.columns = [c[1] if isinstance(c, tuple) else c for c in close.columns]
                    if "Close" in close.columns:
                        close = close[["Close"]]
                    else:
                        close = close.iloc[:, [0]]  # fallback to first col
                    close = close.rename(columns={close.columns[0]: "Close"})

                elif isinstance(close, pd.Series):
                    close = close.to_frame("Close")

                # Reset index so Date is a column
                df_plot = close.reset_index()

                fig = px.line(
                    df_plot,
                    x="Date",
                    y="Close",
                    title=f"{coin} — Close ({lookback})",
                    template=chart_template
                )
                st.plotly_chart(fig, use_container_width=True)



            # ---- Summary table ----
            if metrics_rows:
                mdf = pd.DataFrame(
                    metrics_rows, 
                    columns=["Coin", "Last Price (USD)", f"Return {lookback} %", "Volatility (ann. %)"]
                )
                st.subheader("Summary")
                st.dataframe(mdf, use_container_width=True)

    # ---------------- NEWS (Finnhub + sentiment optional) ----------------
    elif menu == "News":
            st.title("📰 Market News with Sentiment Analysis")

            # List of 25 stocks
            all_symbols = [
                "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
                "NVDA", "META", "NFLX", "INTC", "AMD",
                "IBM", "ORCL", "CSCO", "ADBE", "PYPL",
                "SHOP", "UBER", "LYFT", "SNAP", "SQ",
                "COIN", "SPOT", "BABA", "PDD", "TWTR"
            ]

            # Multi-select dropdown
            selected_stocks = st.multiselect(
                "Select stocks to fetch news for:",
                options=all_symbols,
                default=["AAPL", "MSFT"]
            )

            if st.button("Fetch News"):
                for ticker in selected_stocks:
                    st.subheader(f"📌 {ticker}")
                    news_items = get_news_data(ticker)

                    for n in news_items[:3]:  # top 3 news per stock
                        headline = n.get("headline", "No title")
                        summary = n.get("summary", "")
                        url = n.get("url", "#")  # ✅ get link from API

                        # Run sentiment analysis
                        scores = sentiment_analyzer.polarity_scores(headline)
                        sentiment = (
                            "😊 Positive" if scores['compound'] > 0.05
                            else "😐 Neutral" if scores['compound'] > -0.05
                            else "😟 Negative"
                        )

                        # ✅ Make headline clickable
                        st.markdown(f"**[{headline}]({url})**")
                        st.caption(n.get("datetime", ""))
                        st.write(summary)
                        st.write(f"**Sentiment:** {sentiment}")
                        st.progress((scores['compound'] + 1) / 2)
                        st.markdown("---")

            # Optional chatbot
            try:
                render_chatbot_section()
            except Exception:
                pass




    # ---------------- EXPORT / REPORTS ----------------
    elif menu == "Export/Reports":
        st.header("📤 Export & Weekly Report")
        holdings = current_holdings_df()
        if holdings.empty:
            st.info("Nothing to export yet.")
        else:
            # Enrich
            prices = {t: yf.Ticker(t).history(period="1d")["Close"].iloc[-1] for t in holdings["Ticker"]}
            holdings["Current Price"] = holdings["Ticker"].map(prices)
            holdings["Value"] = holdings["Shares"] * holdings["Current Price"]
            holdings["PnL"] = holdings["Shares"] * (holdings["Current Price"] - holdings["Buy Price"]) 
            # CSV
            csv = holdings.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, file_name="portfolio.csv", mime="text/csv")
            # Excel
            out = BytesIO()
            with pd.ExcelWriter(out, engine='openpyxl') as writer:
                holdings.to_excel(writer, index=False, sheet_name='Portfolio')
            st.download_button("Download Excel", out.getvalue(), file_name="portfolio.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            # Simple text weekly report
            st.subheader("Weekly Summary (preview)")
            week_ago = pd.Timestamp.today() - pd.Timedelta(days=7)
            tickers = holdings["Ticker"].tolist()
            hist = yf.download(tickers=tickers, start=week_ago.date(), progress=False, group_by="ticker")
            perf = []
            for t in tickers:
                try:
                    cclose = hist[(t,'Close')]
                except Exception:
                    cclose = yf.download(t, start=week_ago.date(), progress=False)['Close']
                if len(cclose) >= 2:
                    pct = (cclose.iloc[-1]/cclose.iloc[0]-1)*100
                    perf.append([t, pct])
            if perf:
                perf_df = pd.DataFrame(perf, columns=["Ticker","7D %"]).sort_values("7D %", ascending=False)
                st.dataframe(perf_df, use_container_width=True)

            # ---------------- AI ADVISOR ----------------
    elif menu == "AI Advisor":
        st.header("🤖 AI Advisor")
        st.caption("Educational demo: predicts if a stock is likely to gain >5% over next horizon.")

        # Smaller default set → faster
        universe = st.multiselect(
            "Training universe (⚡ fewer = faster)", 
            list(available_stocks.keys()), 
            default=["AAPL", "MSFT", "NVDA"]
        )

        horizon = st.slider("Forecast horizon (days)", 10, 60, 20, step=5)
        target_thr = st.slider("Target threshold (future %)", 1, 20, 5, step=1) / 100.0
        prob_cut = st.slider("Decision threshold (prob)", 0.40, 0.70, 0.50, step=0.01)

        train_btn = st.button("🧠 Train / Refresh Model")

        if "ml_model" not in st.session_state or train_btn:
            if not universe:
                st.warning("Please select at least one ticker.")
            else:
                with st.spinner(f"Training ML model on {len(universe)} tickers (this may take a while)..."):
                    # progress bar
                    progress = st.progress(0)
                    model, cv_metrics, price_cache = train_ml_model(universe, horizon_days=horizon, target_threshold=target_thr)

                    # manually bump progress bar to 100%
                    progress.progress(100)

                    st.session_state["ml_model"] = model
                    st.session_state["ml_metrics"] = cv_metrics
                    st.session_state["ml_prices"] = price_cache

        model = st.session_state.get("ml_model")
        cv = st.session_state.get("ml_metrics", {})
        prices = st.session_state.get("ml_prices", {})

        if not model:
            st.warning("Training failed or not enough data.")
        else:
            st.subheader("📊 Cross-Validation Metrics")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Samples", f"{cv.get('samples', 0):,}")
            c2.metric("Acc (CV)", f"{cv.get('accuracy', float('nan')):.3f}")
            c3.metric("ROC AUC", f"{cv.get('roc_auc', float('nan')):.3f}")
            c4.metric("Precision", f"{cv.get('precision', float('nan')):.3f}")
            c5.metric("Recall", f"{cv.get('recall', float('nan')):.3f}")

            st.markdown("---")
            st.subheader("🔎 Stock-by-stock prediction")

            test_list = st.multiselect("Evaluate tickers", list(available_stocks.keys()), default=["AAPL","MSFT","NVDA"])
            rows = []
            for t in test_list:
                df = prices.get(t)
                if df is None or df.empty:
                    try:
                        df = yf.Ticker(t).history(period="5y")[["Open","High","Low","Close","Volume"]].dropna()
                    except Exception:
                        df = pd.DataFrame()
                res = predict_signal(model, df, horizon_days=horizon, threshold_prob=prob_cut)
                if res:
                    rows.append([t, res["prob"], res["label"]])
            if rows:
                pred_df = pd.DataFrame(rows, columns=["Ticker","Invest Probability","Signal"]).sort_values("Invest Probability", ascending=False)

                st.dataframe(pred_df, use_container_width=True)

       
    
    elif menu == "Compare":
        st.header("📊 Compare Stocks & Portfolios")
        try:
            tickers = st.multiselect("Select stocks to compare", options=list(available_stocks.keys()))
            selected_portfolios = st.multiselect("Select portfolios to compare", options=list(portfolios_df.keys()))
            if tickers:
                import yfinance as yf
                import pandas as pd
                import plotly.express as px
                data = {}
                for t in tickers:
                    hist = yf.download(t, period="1y")["Adj Close"]
                    data[t] = hist
                df = pd.DataFrame(data)
                st.line_chart(df)
                perf = (df.iloc[-1] / df.iloc[0] - 1).round(3)
                st.write("**Stock Returns (1Y):**", perf)
            if selected_portfolios:
                pf_values = {}
                for pf in selected_portfolios:
                    pf_df = portfolios_df.get(pf, pd.DataFrame())
                    if not pf_df.empty:
                        pf_values[pf] = pf_df["Value"].values if "Value" in pf_df else []
                if pf_values:
                    st.write("**Portfolio comparison loaded.**")
                    # Simplified placeholder, you can extend to show charts
                    st.write(pf_values)
        except Exception as e:
            st.error(f"Error in Compare: {e}")

    elif menu == "Logout":
            st.session_state["authenticated"] = False
            st.session_state["user"] = None
            st.rerun()


# ==================== ADDED: Render Floating Chatbot (persistent) ====================
try:
    _floating_chat_ui()
except Exception as _e:
    pass
# ==================== END ADDED ====================
