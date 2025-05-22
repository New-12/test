import socket

SERVER_IP = "PC'nin_İP_adresi"  # Örn: "192.168.1.10" veya public IP
SERVER_PORT = 9999

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    print("[*] Sunucuya bağlandı")

    while True:
        komut = input("Komut gönder: ")
        if komut == "/cikis":
            print("Bağlantı kapatılıyor")
            client.sendall("/kapat".encode('utf-8'))
            break
        client.sendall(komut.encode('utf-8'))
        cevap = client.recv(4096).decode('utf-8')
        print(f"Sunucu: {cevap}")

    client.close()

if __name__ == "__main__":
    start_client()
