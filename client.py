import socket

HOST = '127.0.0.1'
PORT = 65432

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        while True:
            cmd = input("Enter command (REFRESH) or type EXIT: ")
            if cmd.lower() == "exit":
                break
            client_socket.sendall(cmd.encode())
            response = client_socket.recv(1024).decode()
            print(f"Server Response: {response}")

if __name__ == "__main__":
    main()
