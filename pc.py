import socket
import threading
import os

HOST = "0.0.0.0"  # Tüm IP adreslerinden bağlantı kabul et
PORT = 65432

def handle_client(conn, addr):
    print(f"Bağlantı kuruldu: {addr}")
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Gelen komut: {data}")

            if data == "/foto":
                # Fotoğraf çekme komutu, telefon yapacak, burada sadece onay veriyoruz
                conn.send("FOTO".encode())

            elif data.startswith("/dosya_gonder"):
                # Örnek: /dosya_gonder dosya_adi.txt
                _, filename = data.split(maxsplit=1)
                if os.path.exists(filename):
                    with open(filename, "rb") as f:
                        content = f.read()
                    conn.send(b"FILESTART" + content + b"FILEEND")
                else:
                    conn.send(b"FILE_NOT_FOUND")

            elif data == "/baglan":
                conn.send("BAGLANILDI".encode())

            else:
                conn.send("BILINMEYEN_KOMUT".encode())

        except:
            break
    conn.close()
    print(f"Bağlantı kapandı: {addr}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Sunucu {HOST}:{PORT} üzerinde dinleniyor...")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    main()
