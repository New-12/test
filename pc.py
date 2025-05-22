import socket
import os

def send_command(sock, cmd):
    sock.sendall(cmd.encode())

def recv_data(sock):
    data = b""
    while True:
        packet = sock.recv(4096)
        if not packet:
            break
        data += packet
    return data

def receive_file(sock, filename):
    with open(filename, "wb") as f:
        while True:
            data = sock.recv(4096)
            if not data:
                break
            f.write(data)

def send_file(sock, filepath):
    with open(filepath, "rb") as f:
        while True:
            bytes_read = f.read(4096)
            if not bytes_read:
                break
            sock.sendall(bytes_read)

def main():
    pc_ip = "0.0.0.0"  # Dinleme için tüm arayüzler
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((pc_ip, port))
    server_socket.listen(1)
    print(f"Sunucu dinlemede: {pc_ip}:{port}")

    conn, addr = server_socket.accept()
    print(f"Bağlantı geldi: {addr}")

    while True:
        cmd = input("Komut (/foto, /dosya-gonder dosyaadi, /dosya-al dosyaadi, /quit): ")
        if cmd == "/quit":
            send_command(conn, "/quit")
            break

        if cmd.startswith("/dosya-gonder "):
            filename = cmd.split(" ", 1)[1]
            if not os.path.exists(filename):
                print("Dosya bulunamadı.")
                continue
            send_command(conn, cmd)
            print(f"Dosya gönderiliyor: {filename}")
            send_file(conn, filename)
            print("Dosya gönderimi tamamlandı.")

        elif cmd.startswith("/dosya-al "):
            filename = cmd.split(" ", 1)[1]
            send_command(conn, cmd)
            print(f"Dosya alınıyor: {filename}")
            receive_file(conn, filename)
            print("Dosya alımı tamamlandı.")

        elif cmd == "/foto":
            send_command(conn, "/foto")
            print("Fotoğraf bekleniyor...")
            receive_file(conn, "telefon_fotografi.jpg")
            print("Fotoğraf alındı: telefon_fotografi.jpg")

        else:
            send_command(conn, cmd)
            print("Bilinmeyen komut.")

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    main()
