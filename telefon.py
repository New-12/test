import socket

# Kullanıcıdan PC'nin IP adresini alıyoruz
pc_ip = input("Bağlanmak istediğiniz PC'nin IP adresini girin: ")
port = 12345  # pc.py ile aynı port olmalı

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((pc_ip, port))
        print(f"[+] {pc_ip}:{port} adresine bağlanıldı.")

        while True:
            komut = input("Komut girin (/foto, /dosya, çıkmak için 'exit'): ")

            if komut.lower() == 'exit':
                break

            client.sendall(komut.encode())

            cevap = client.recv(4096).decode()
            print(f"PC'den cevap: {cevap}")

    except Exception as e:
        print(f"Hata: {e}")
    finally:
        client.close()
        print("Bağlantı kapandı.")

if __name__ == "__main__":
    main()
