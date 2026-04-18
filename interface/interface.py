from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Label, RichLog, Footer, Static
from textual.screen import Screen

import threading
from core import server, client
from utils import broadcast, room_config

ROOM_CODE = ""
ROOM_NAME = ""
display_name = "guest01"
display_color = "green"

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        # startup screen buttons
        yield Button("Host", id="host")
        yield Button("Join", id="join")
        yield Button("Settings", id="settings")
        yield Button("Exit", id="exit")

        # host or join screen input fields and buttons
        yield Label("", id="room_details")
        yield Input(placeholder="Room Code", id="room_code")
        yield Button("Create", id="create_room")
        yield Button("Join", id="join_room")

        # settings screen fields and buttons
        yield Input(placeholder="change your name", id="display_name")
        yield Input(placeholder="change your color", id="display_color")
        yield Button("Update", id="update")

        # multi screen back button
        yield Button("Back", id="back")

        yield Footer()

    def on_mount(self):
        self.query_one("#room_details").display = False
        self.query_one("#room_code").display = False
        self.query_one("#create_room").display = False
        self.query_one("#join_room").display = False

        self.query_one("#display_name").display = False
        self.query_one("#display_color").display = False
        self.query_one("#update").display = False

        self.query_one("#back").display = False
        # more settings fields and buttons here

        self.discovered_host_ip = None
        self.discovered_room_code = None
        self.discovered_room_name = None

    def on_screen_resume(self):
        self.query_one("#host").display = True
        self.query_one("#join").display = True
        self.query_one("#settings").display = True
        self.query_one("#exit").display = True

        self.query_one("#room_details").display = False
        self.query_one("#room_code").display = False
        self.query_one("#create_room").display = False
        self.query_one("#join_room").display = False
        self.query_one("#display_name").display = False
        self.query_one("#display_color").display = False
        self.query_one("#update").display = False
        self.query_one("#back").display = False

    def _handle_host_fields(self, host_ip, room_code, room_name):
        self.discovered_host_ip = host_ip
        self.discovered_room_code = room_code
        self.discovered_room_name = room_name

    def auto_discover_host(self):
        host_ip, room_code, room_name = broadcast.listen_for_host()
        self.app.call_from_thread(self._handle_host_fields, host_ip, room_code, room_name)


    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "exit":
            self.app.exit()

        elif event.button.id == "settings":
            self.query_one("#host").display = False
            self.query_one("#join").display = False
            self.query_one("#settings").display = False
            self.query_one("#exit").display = False

            self.query_one("#display_name").display = True
            self.query_one("#display_color").display = True
            self.query_one("#update").display = True
            self.query_one("#back").display = True
            # A label is needed to display the current name and get update when update is pressed.

        elif event.button.id == "update":
            global display_name, display_color
            display_name = self.query_one("#display_name", Input).value
            display_color = self.query_one("#display_color", Input).value

        elif event.button.id == "back":
            self.query_one("#host").display = True
            self.query_one("#join").display = True
            self.query_one("#settings").display = True
            self.query_one("#exit").display = True

            self.query_one("#room_details").display = False
            self.query_one("#room_code").display = False
            self.query_one("#create_room").display = False
            self.query_one("#join_room").display = False
            self.query_one("#display_name").display = False
            self.query_one("#display_color").display = False
            self.query_one("#update").display = False
            self.query_one("#back").display = False

        elif event.button.id == "host":
            global ROOM_CODE, ROOM_NAME
            ROOM_CODE = room_config.generate_room_code()
            ROOM_NAME = room_config.generate_room_name()

            self.query_one("#host").display = False
            self.query_one("#join").display = False
            self.query_one("#settings").display = False
            self.query_one("#exit").display = False

            self.query_one("#room_details").display = True
            self.query_one("#create_room").display = True
            self.query_one("#back").display = True

            self.query_one("#room_details", Label).update(f"ROOM CODE: {ROOM_CODE}\tROOM NAME: {ROOM_NAME}")

        elif event.button.id == "join":
            threading.Thread(target=self.auto_discover_host, daemon=True).start()

            self.query_one("#host").display = False
            self.query_one("#join").display = False
            self.query_one("#settings").display = False
            self.query_one("#exit").display = False

            self.query_one("#room_code").display = True
            self.query_one("#join_room").display = True
            self.query_one("#back").display = True

        elif event.button.id == "create_room":
            threading.Thread(target=server.start_server, args=(ROOM_CODE,), daemon=True).start()
            threading.Thread(target=broadcast.start_broadcasting, args=(ROOM_CODE, ROOM_NAME), daemon=True).start()
            client.connect(host="127.0.0.1", port=5000, username=display_name, color=display_color, room_code=ROOM_CODE)

            self.app.push_screen(ChatScreen(display_name, display_color))
            self.notify("room created.")

        elif event.button.id == "join_room":
            room_code = self.query_one("#room_code", Input).value
            HOST_IP = self.discovered_host_ip
            ROOM_CODE = self.discovered_room_code
            ROOM_NAME = self.discovered_room_name

            if not HOST_IP:
                self.notify("Host not found yet.")
                return
            else:
                if room_code == ROOM_CODE:
                    try:
                        client.connect(host=HOST_IP, port=5000, username=display_name, color=display_color, room_code=room_code)

                        self.app.push_screen(ChatScreen(display_name, display_color))
                        self.notify(f"{ROOM_NAME} joined.")
                    except Exception:
                        self.notify("Failed to connect.")
                else:
                    self.notify("Incorrect password")


class ChatScreen(Screen):
    def __init__(self, name, color):
        super().__init__()
        self.user = name
        self.color = color

    def compose(self) -> ComposeResult:
        yield Static(id="header")
        yield RichLog(id="messages", markup=True)
        yield Input(placeholder="Type a message...", id="message_input")
        yield Button("Leave", id="leave")

    def on_mount(self):
        self.query_one("#header", Static).update(f"Room Name: [bold]{ROOM_NAME}[/bold]\t\t\t ━━━ \t\t\tRoom Code: [bold]{ROOM_CODE}[/bold]")
        self.query_one("#message_input").focus()
        threading.Thread(target=client.receive_message, args=(self.display_message,), daemon=True).start()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "leave":
            client.send_leave(self.user, self.color)
            self.app.pop_screen()

    def on_input_submitted(self, event: Input.Submitted):
        log = self.query_one("#messages", RichLog)
        log.write(f"[{self.color}]{self.user}[/{self.color}] > {event.value}")
        client.send_message(self.user, self.color, event.value)
        event.input.clear()

    def _write_message(self, message):
        log = self.query_one("#messages", RichLog)
        log.write(message)

    def display_message(self, message):
        self.app.call_from_thread(self._write_message, message)

class LaternApp(App):
    CSS_PATH = "lantern.tcss"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("up", "focus_previous", "Up"),
        ("down", "focus_next", "Down"),
        # ("escape", "back", "Back"),
    ]

    def on_mount(self):
        self.push_screen(HomeScreen())
