import socket
import time
from core import protocol


def start_broadcasting(room_code, room_name, broadcast_ip="255.255.255.255", broadcast_port=5001):
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_message = {"room_code": room_code, "room_name": room_name}
    encoded_broadcast = protocol.encode(broadcast_message)

    while True:
        try:
            broadcast_socket.sendto(encoded_broadcast, (broadcast_ip, broadcast_port))
        except Exception:
            pass
        time.sleep(1)


def listen_for_host():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", 5001))
    data, address = udp_socket.recvfrom(1024)
    udp_decoded = protocol.decode(data)

    host_ip = address[0]
    room_code = udp_decoded.get("room_code")
    room_name = udp_decoded.get("room_name")

    return host_ip, room_code, room_name
