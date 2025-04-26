# 📈 Finance Tracker MCP Server

A lightweight Python MCP (Multi-Client Platform) server that tracks stock portfolio information in real time.  
It fetches **live data** using [Yahoo Finance](https://finance.yahoo.com/) (via `yfinance`) and **updates Google Sheets** automatically with portfolio performance, gain/loss calculations, and clean formatting.

---

## 📚 Features

- 🛜 Multi-client TCP server (built with Python `socket`)
- 📈 Fetches **live stock prices** and financial data using `yfinance`
- 🧮 Calculates gains, losses, percent changes, total portfolio value
- 📋 Uploads and formats **Google Sheets** automatically
- 🟢 Green/Red formatting based on gain/loss
- 🔄 `REFRESH` command to instantly update your portfolio
- 🔒 Protects sensitive files with `.gitignore`

---

## 🛠️ Technology Stack

- Python 3.9+
- `socket` (for MCP server)
- `yfinance`
- `gspread`
- `oauth2client`
- `gspread-formatting`
- Google Sheets API
- Google Drive API

---

## 🚀 Installation Guide

### 1. Clone the repository
```bash
git clone https://github.com/kosungjunmichael/finance_tracker.git
cd finance_tracker
