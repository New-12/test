import socket
import os

PORT = 65432
CONFIG_FILE = "config.txt"

def get_pc_ip():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            ip = f.read().strip()
            if ip:
                return ip

    ip = input("Lütfen PC IP adresini girin : ").strip()
    with open(CONFIG_FILE, "w") as f:
        f.write(ip)
    return ip

def main():
    pc_ip = 192.168.1.107()
    print(f"PC IP adresi: 192.168.1.107")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((pc_ip, PORT))
            print("PC'ye bağlanıldı.")
        except Exception as e:
            print("Bağlanırken hata:", e)
            return

        while True:
            komut = input("Komut gir (/foto, /dosya_gonder dosya_adi.txt, çıkış için q): ").strip()

            if komut.lower() == "q":
                print("Bağlantı sonlandırıldı.")
                break

            s.send(komut.encode())
            data = s.recv(1024)

            if data == b"FOTO":
                print("Fotoğraf çekme komutu gönderildi. (Burada telefon kamerayı açacak)")

            elif data.startswith(b"FILESTART"):
                content = data[9:]
                # Eğer dosya büyükse bu basit haliyle yetmeyebilir, iyileştirilebilir
                filename = komut.split(maxsplit=1)[1]
                with open(filename, "wb") as f:
                    f.write(content)
                print(f"{filename} dosyası alındı.")

            elif data == b"FILE_NOT_FOUND":
                print("Dosya bulunamadı.")

            else:
                print("Sunucudan cevap:", data.decode())

if __name__ == "__main__":
    main()
