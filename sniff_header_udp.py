import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 20777))

print("monitorando header...")

while True:
    data, _ = sock.recvfrom(4096)

    print("size:", len(data), "| first bytes:", list(data[:15]))
