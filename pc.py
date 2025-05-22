import socket
import threading

HOST = '0.0.0.0'  # Tüm IP'lerden bağlantı kabul
PORT = 9999       # Dilediğin port

clients = []

def handle_client(client_socket, addr):
    print(f"[+] Yeni bağlanan: {addr}")
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print(f"[-] {addr} bağlantısı kapandı")
                break
            print(f"[{addr}] Komut: {data}")
            
            if data == "/ip":
                # Telefonun IP'sini istemek için
                client_socket.sendall(f"IP'n: {addr[0]}".encode('utf-8'))

            elif data == "/kapat":
                print(f"[-] {addr} bağlantısı kapatılıyor...")
                break

            else:
                client_socket.sendall("Bilinmeyen komut".encode('utf-8'))
        except:
            break

    client_socket.close()
    print(f"[-] Bağlantı sonlandırıldı: {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Sunucu {HOST}:{PORT} dinleniyor...")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
