import socket
import struct
import csv
import time
import os

UDP_IP = "0.0.0.0"
UDP_PORT = 20777

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Escutando Session + LapData + Telemetry...")

# =========================
# ESTADO GLOBAL
# =========================

current_lap = -1
writer = None
file = None
start = time.time()

session_info = {}


# =========================
# FUNÇÕES AUXILIARES
# =========================

def read_packet_id(data):
    return struct.unpack_from("<B", data, 5)[0]


# ---------- SESSION ----------
def parse_session(data):
    track_temp = struct.unpack_from("<b", data, 25)[0]
    air_temp = struct.unpack_from("<b", data, 26)[0]
    weather = struct.unpack_from("<B", data, 24)[0]

    session_info["track_temp"] = track_temp
    session_info["air_temp"] = air_temp
    session_info["weather"] = weather

    print("Session:", session_info)


# ---------- LAP ----------
def parse_lap(data):
    global current_lap, writer, file

    offset = 29  # primeiro carro

    lap_num = struct.unpack_from("<B", data, offset + 2)[0]
    lap_time = struct.unpack_from("<f", data, offset)[0]

    if lap_num != current_lap:
        current_lap = lap_num

        if file:
            file.close()

        os.makedirs("laps", exist_ok=True)

        file = open(f"laps/lap_{lap_num}.csv", "w", newline="")
        writer = csv.writer(file)

        writer.writerow([
            "time",
            "speed",
            "throttle",
            "brake",
            "gear",
            "rpm",
            "lap_time",
            "track_temp",
            "air_temp"
        ])

        print(f"Nova volta detectada: {lap_num} | lap_time={lap_time:.3f}")


# ---------- TELEMETRY ----------
def parse_telemetry(data):
    offset = 29

    speed = struct.unpack_from("<H", data, offset)[0]
    throttle = struct.unpack_from("<f", data, offset + 2)[0]
    brake = struct.unpack_from("<f", data, offset + 6)[0]
    gear = struct.unpack_from("<b", data, offset + 14)[0]
    rpm = struct.unpack_from("<H", data, offset + 15)[0]

    return speed, throttle, brake, gear, rpm


# =========================
# LOOP PRINCIPAL
# =========================

while True:
    data, _ = sock.recvfrom(4096)
    packet_id = read_packet_id(data)

    if packet_id == 1:
        parse_session(data)

    elif packet_id == 2:
        parse_lap(data)

    elif packet_id == 6 and writer:
        speed, throttle, brake, gear, rpm = parse_telemetry(data)

        t = time.time() - start

        writer.writerow([
            round(t, 3),
            speed,
            throttle,
            brake,
            gear,
            rpm,
            "",
            session_info.get("track_temp", ""),
            session_info.get("air_temp", "")
        ])

        file.flush()
