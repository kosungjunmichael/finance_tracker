from mcp_tools import ToolServer, ToolFunction
from company_info import CompanyInfo
from google_sheets import GoogleSheetHandler
import json

# Load your config file
with open("config.json", "r") as f:
    config = json.load(f)

portfolio = config["stocks"]
portfolio_dict = {s["ticker"]: {"purchase_price": s["purchase_price"], "shares": s["shares"]} for s in portfolio}
info_fetcher = CompanyInfo(portfolio)
sheet_handler = GoogleSheetHandler(config["sheet_name"])

@ToolFunction()
def refresh_portfolio():
    stock_data = info_fetcher.fetch_all_data()
    sheet_handler.update_sheet(stock_data, portfolio_dict)
    return {
        "status": "success",
        "message": f"{len(stock_data)} stocks updated in Google Sheets"
    }

if __name__ == "__main__":
    server = ToolServer()
    server.add_tool(refresh_portfolio)
    server.run_stdio()
