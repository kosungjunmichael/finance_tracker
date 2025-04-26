import gspread
from google.oauth2.service_account import Credentials
from gspread_formatting import *
import datetime

class GoogleSheetHandler:
    def __init__(self, sheet_name):
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = Credentials.from_service_account_file('service_account.json', scopes=scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(sheet_name).sheet1

    def update_sheet(self, stock_data, portfolio_data):
        """Fully refresh the Google Sheet."""
        self.sheet.clear()
        
        headers = ['Ticker', 'Name', 'Current Price', 'Purchase Price', 
                   'Shares', 'Total Cost', 'Current Value', '% Change', 'Gain/Loss']
        self.sheet.update('A1:I1', [headers])

        # Format header
        header_format = CellFormat(
            backgroundColor=Color(0.9, 0.9, 0.9),
            textFormat=TextFormat(bold=True),
            horizontalAlignment='CENTER'
        )
        format_cell_range(self.sheet, '1:1', header_format)

        # Fill in the stock rows
        rows = []
        row_idx = 2
        for ticker, stock_info in stock_data.items():
            purchase_price = portfolio_data[ticker]['purchase_price']
            shares = portfolio_data[ticker]['shares']

            current_price = stock_info['current_price']
            total_cost = purchase_price * shares
            current_value = current_price * shares
            percent_change = ((current_price - purchase_price) / purchase_price) * 100 if purchase_price > 0 else 0
            gain_loss = current_value - total_cost

            row = [
                ticker,
                stock_info['name'],
                current_price,
                purchase_price,
                shares,
                total_cost,
                current_value,
                percent_change / 100,
                gain_loss
            ]
            rows.append(row)

            # Color formatting
            if stock_info['price_increased']:
                cell_format = CellFormat(backgroundColor=Color(0.85, 0.95, 0.85))  # Light green
            else:
                cell_format = CellFormat(backgroundColor=Color(0.95, 0.85, 0.85))  # Light red
            format_cell_range(self.sheet, f'C{row_idx}', cell_format)

            # Color formatting for gain/loss
            if percent_change > 0:
                cell_format = CellFormat(backgroundColor=Color(0.85, 0.95, 0.85))
            else:
                cell_format = CellFormat(backgroundColor=Color(0.95, 0.85, 0.85))
            format_cell_range(self.sheet, f'H{row_idx}:I{row_idx}', cell_format)

            row_idx += 1

        if rows:
            self.sheet.update(f'A2:I{len(rows)+1}', rows)

        # Currency formatting
        currency_format = CellFormat(numberFormat=NumberFormat(type='CURRENCY', pattern='$#,##0.00'))
        format_cell_range(self.sheet, 'C:D', currency_format)
        format_cell_range(self.sheet, 'F:G', currency_format)
        format_cell_range(self.sheet, 'I:I', currency_format)

        # Percentage formatting
        percent_format = CellFormat(numberFormat=NumberFormat(type='PERCENT', pattern='0.00%'))
        format_cell_range(self.sheet, 'H:H', percent_format)

        # Total Row
        total_row = len(rows) + 2
        self.sheet.update_cell(total_row, 1, "TOTAL")
        self.sheet.update_cell(total_row, 6, f'=SUM(F2:F{total_row-1})')
        self.sheet.update_cell(total_row, 7, f'=SUM(G2:G{total_row-1})')
        self.sheet.update_cell(total_row, 9, f'=SUM(I2:I{total_row-1})')

        # Total row formatting
        total_format = CellFormat(
            textFormat=TextFormat(bold=True),
            backgroundColor=Color(0.9, 0.9, 0.9)
        )
        format_cell_range(self.sheet, f'{total_row}:{total_row}', total_format)

        # Timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.sheet.update_cell(total_row + 2, 1, f"Last Updated: {timestamp}")
