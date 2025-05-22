import socket
import cv2
import os

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

def capture_photo():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()
    if ret:
        cv2.imwrite("foto.jpg", frame)
        return True
    else:
        return False

def main():
    # PC'nin ip adresini burada parametre olarak ver (telefon pc'ye bağlanacak)
    pc_ip = "PC_IP_BURAYA"  # Örn: "192.168.1.10"
    port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((pc_ip, port))
    print(f"{pc_ip}:{port} adresine bağlandı.")

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break

        if data == "/quit":
            print("Sunucu bağlantıyı kapattı.")
            break

        elif data == "/foto":
            print("Fotoğraf çekiliyor...")
            if capture_photo():
                client_socket.sendall(b"START")
                with open("foto.jpg", "rb") as f:
                    while True:
                        bytes_read = f.read(4096)
                        if not bytes_read:
                            break
                        client_socket.sendall(bytes_read)
                print("Fotoğraf gönderildi.")
            else:
                print("Fotoğraf çekilemedi.")

        elif data.startswith("/dosya-gonder "):
            filename = data.split(" ", 1)[1]
            if os.path.exists(filename):
                client_socket.sendall(b"START")
                with open(filename, "rb") as f:
                    while True:
                        bytes_read = f.read(4096)
                        if not bytes_read:
                            break
                        client_socket.sendall(bytes_read)
                print(f"{filename} dosyası gönderildi.")
            else:
                print(f"{filename} bulunamadı.")

        elif data.startswith("/dosya-al "):
            filename = data.split(" ", 1)[1]
            print(f"Dosya alınıyor: {filename}")
            with open(filename, "wb") as f:
                while True:
                    data_file = client_socket.recv(4096)
                    if not data_file:
                        break
                    f.write(data_file)
            print(f"{filename} dosyası alındı.")

        else:
            print(f"Bilinmeyen komut: {data}")

    client_socket.close()

if __name__ == "__main__":
    main()
