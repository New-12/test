import socket
import threading

HOST = '0.0.0.0'  # Tüm IP'lerden bağlantı kabul eder
PORT = 12345      # İstersen değiştirilebilir

def handle_client(conn, addr):
    print(f"[+] Bağlantı kuruldu: {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            mesaj = data.decode()
            print(f"Telefon'dan gelen: {mesaj}")

            # Örnek komutlar
            if mesaj.startswith('/foto'):
                # Fotoğraf çekme veya başka işlem buraya eklenebilir
                cevap = "Fotoğraf çekildi (örnek cevap)"
                conn.sendall(cevap.encode())

            elif mesaj.startswith('/dosya'):
                # Dosya gönderme işlemi burada olabilir
                cevap = "Dosya gönderiliyor (örnek cevap)"
                conn.sendall(cevap.encode())

            else:
                conn.sendall(b"Komut anlasilmadi.")
    finally:
        conn.close()
        print(f"[-] Bağlantı kapandı: {addr}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[+] Sunucu {HOST}:{PORT} üzerinde dinliyor...")

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
