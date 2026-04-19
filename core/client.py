import socket
from core import protocol
import time


def connect(host, port, username, color, room_code):
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for _ in range(5):
        try:
            client_socket.connect((host, port))
            break
        except ConnectionRefusedError:
            time.sleep(0.3)

    join_request = {"type": "join", "username": username, "color": color, "room_code": room_code}
    encoded_request = protocol.encode(join_request)
    client_socket.send(encoded_request)

def send_message(username, color, message_text):
    message_send = {"type": "chat", "username": username, "color": color, "message": message_text}
    encoded_message = protocol.encode(message_send)
    client_socket.send(encoded_message)

def send_leave(username, color):
    leave_message = {"type": "leave", "username": username, "color": color}
    encoded_leave = protocol.encode(leave_message)
    try:
        client_socket.send(encoded_leave)
    except Exception:
        pass

def receive_message(callback, user_callback):
    while True:
        try:
            message_receive = client_socket.recv(1024)
            decoded_receive = protocol.decode(message_receive)
            message_sender = decoded_receive.get("username")
            message_color = decoded_receive.get("color")
            if decoded_receive.get("type") == "join":
                callback(f"{message_sender} - Joined")
                user_callback(message_sender, message_color, "join")
            elif decoded_receive.get("type") == "leave":
                callback(f"{message_sender} - Left")
                user_callback(message_sender, message_color, "leave")
            else:
                message_content = decoded_receive.get("message")
                callback(f"[{message_color}]{message_sender}[/{message_color}] - {message_content}")
        except Exception:
            break
