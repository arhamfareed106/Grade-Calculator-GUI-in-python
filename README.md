# 📈 Stock Price Analyzer (Tkinter + yFinance)

A lightweight Python desktop application that fetches, visualizes, and exports stock market data using a clean **Tkinter-based GUI**. Built for educational, freelance, and exam-level use.

---

## 🚀 Features

- ✅ Fetch historical stock data using [`yfinance`](https://pypi.org/project/yfinance/)
- 📅 Choose from 7, 30, or 90-day durations
- 📊 Interactive graphs with:
  - Open and Close prices
  - Optional **SMA-10** (Simple Moving Average)
- 🧾 Tabular display of OHLC data
- 💾 Export stock data as `.csv`
- 💡 Auto-suggest ticker symbols for common companies
- 🌕 Clean light theme using `ttk` styling
- 🧪 Error handling and data validation included

---

## 🖼️ GUI Preview

![App Screenshot](screenshot.png) <!-- Add an actual screenshot file in your repo -->

---

## 🧱 Tech Stack

| Component        | Library          |
|------------------|------------------|
| GUI              | `tkinter`, `ttk` |
| Data Source      | `yfinance`       |
| Data Handling    | `pandas`         |
| Plotting         | `matplotlib`     |
| File Export      | `csv`, `tkinter.filedialog` |

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/stock-analyzer.git
cd stock-analyzer

# 2. Install dependencies
pip install yfinance pandas matplotlib

# 3. Run the app
python main.py
