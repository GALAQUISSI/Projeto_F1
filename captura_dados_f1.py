import socket
import csv
import time
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 20777))

print("Capturando pacotes do F1 25...")

os.makedirs("packets", exist_ok=True)

files = {
    0: open("packets/motion.csv", "w", newline=""),
    1: open("packets/session.csv", "w", newline=""),
    2: open("packets/lap.csv", "w", newline=""),
    3: open("packets/events.csv", "w", newline=""),
    5: open("packets/setup.csv", "w", newline = ""),
    6: open("packets/telemetry.csv", "w", newline=""),
    7: open("packets/status.csv", "w", newline=""),
    10: open("packets/car_damage.csv", "w", newline=""),
    11: open("packets/history.csv", "w", newline=""),
    12: open("packets/tyre_extended.csv", "w", newline=""),
    14: open("packets/time_trial.csv", "w", newline="")
}

writers = {k: csv.writer(v) for k, v in files.items()}

for w in writers.values():
    w.writerow(["time", "size", "raw_hex"])


start = time.time()


def packet_id(data):
    return data[6]  


while True:
    # data, _, esse _ é o endereço do remetente
    data, _ = sock.recvfrom(4096)

    pid = packet_id(data)

    if pid in writers:
        t = time.time() - start

        writers[pid].writerow([
            round(t, 3),
            len(data),
            data.hex()
        ])

        files[pid].flush()
