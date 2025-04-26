import yfinance as yf

class CompanyInfo:
    def __init__(self, portfolio):
        self.portfolio = portfolio  # Loaded from config.json

    def fetch_all_data(self):
        """Fetch current stock info for all portfolio stocks."""
        stock_data = {}
        for item in self.portfolio:
            ticker = item['ticker']
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                prev_close = info.get('previousClose', 0)
                stock_data[ticker] = {
                    'current_price': current_price,
                    'prev_close': prev_close,
                    'price_increased': current_price > prev_close,
                    'name': info.get('shortName', ticker)
                }
            except Exception as e:
                stock_data[ticker] = {
                    'current_price': 0,
                    'prev_close': 0,
                    'price_increased': False,
                    'name': ticker
                }
        return stock_data
