# run_tracker.py
from company_info import CompanyInfo
from google_sheets import GoogleSheetHandler
import json

def main():
    with open("config.json", "r") as f:
        config = json.load(f)

    sheet_name = config["sheet_name"]
    stocks = config["stocks"]

    portfolio_dict = {
        stock["ticker"]: {
            "purchase_price": stock["purchase_price"],
            "shares": stock["shares"]
        } for stock in stocks
    }

    info_fetcher = CompanyInfo(stocks)
    sheet_handler = GoogleSheetHandler(sheet_name)

    print("📈 Fetching stock data...")
    stock_data = info_fetcher.fetch_all_data()

    print("📤 Updating Google Sheet...")
    sheet_handler.update_sheet(stock_data, portfolio_dict)

    print(f"✅ Updated {len(stock_data)} stocks to sheet: {sheet_name}")

if __name__ == "__main__":
    main()
