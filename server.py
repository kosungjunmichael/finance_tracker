import socket
import threading
import json
from company_info import CompanyInfo
from google_sheets import GoogleSheetHandler

HOST = '0.0.0.0'
PORT = 65432

with open('config.json', 'r') as f:
    config = json.load(f)

portfolio = config['stocks']
portfolio_dict = {stock['ticker']: {'purchase_price': stock['purchase_price'], 'shares': stock['shares']} for stock in portfolio}

info_fetcher = CompanyInfo(portfolio)
sheet_handler = GoogleSheetHandler(config['sheet_name'])

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    with conn:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"[Request] {data}")
            if data.strip().upper() == "REFRESH":
                stock_data = info_fetcher.fetch_all_data()
                sheet_handler.update_sheet(stock_data, portfolio_dict)
                conn.sendall("Sheet refreshed!".encode())
            else:
                conn.sendall("Unknown command. Use REFRESH.".encode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    main()
