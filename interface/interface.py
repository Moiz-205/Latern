from textual.app import App, ComposeResult
from textual.widgets import Input, Button, RichLog
from textual.screen import Screen


ROOM = "000"    # room-code
HOST = "000"    # host-ip

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        # startup screen buttons
        yield Button("Host", id="host")
        yield Button("Join", id="join")
        yield Button("Settings", id="settings")
        yield Button("Exit", id="exit")
        # host or join screen input fields and buttons
        yield Input(placeholder="Name", id="name")
        yield Input(placeholder="Color", id="color")
        yield Input(placeholder="Room Code", id="room_code")
        yield Input(placeholder="Host IP", id="host_ip")
        yield Button("Create", id="create_room")
        yield Button("Join", id="join_room")
        yield Button("Back", id="back")
        # settings screen fields and buttons


    def on_mount(self):
        self.query_one("#name").display = False
        self.query_one("#color").display = False
        self.query_one("#room_code").display = False
        self.query_one("#host_ip").display = False
        self.query_one("#create_room").display = False
        self.query_one("#join_room").display = False
        self.query_one("#back").display = False
        # more settings fields and buttons here

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "host":
            self.query_one("#host").display = False
            self.query_one("#join").display = False
            self.query_one("#settings").display = False
            self.query_one("#exit").display = False

            self.query_one("#name").display = True
            self.query_one("#color").display = True
            self.query_one("#create_room").display = True
            self.query_one("#back").display = True

            # here, randomly generated room code is displayed
            # upon selecting enter, host joins the chat and room is created
            # and host_ip is broadcasted (later UDP functionality)

        elif event.button.id == "join":
            self.query_one("#host").display = False
            self.query_one("#join").display = False
            self.query_one("#settings").display = False
            self.query_one("#exit").display = False

            self.query_one("#name").display = True
            self.query_one("#color").display = True
            self.query_one("#room_code").display = True
            self.query_one("#host_ip").display = True
            self.query_one("#join_room").display = True
            self.query_one("#back").display = True

        elif event.button.id == "settings":
            self.notify("settings pressed")

        elif event.button.id == "exit":
            self.app.exit()

        elif event.button.id == "back":
            self.query_one("#host").display = True
            self.query_one("#join").display = True
            self.query_one("#settings").display = True
            self.query_one("#exit").display = True

            self.query_one("#name").display = False
            self.query_one("#color").display = False
            self.query_one("#room_code").display = False
            self.query_one("#host_ip").display = False
            self.query_one("#create_room").display = False
            self.query_one("#join_room").display = False
            self.query_one("#back").display = False

        elif event.button.id == "create_room":
            # check condition is user can be host or is user actually able to host
            # like connected to hotspot or LAN.
            # if it is true then host will display its hosting_ip and create a room.
            # (in this case host will be broadcasting its ip UDP Broadcast)
            name = self.query_one("#name", Input).value
            color = self.query_one("#color", Input).value

            self.app.push_screen(ChatScreen(name, color))
            self.notify("room created.")

        elif event.button.id == "join_room":
            room_code = self.query_one("#room_code", Input).value
            host_ip = self.query_one("#host_ip", Input).value

            name = self.query_one("#name", Input).value
            color = self.query_one("#color", Input).value

            if room_code == ROOM and host_ip == HOST:
                self.app.push_screen(ChatScreen(name, color))
                self.notify("chat joined.")
            else:
                self.notify("Red")


class ChatScreen(Screen):
    def __init__(self, name, color):
        super().__init__()
        self.user = name
        self.color = color

    def compose(self) -> ComposeResult:
        yield RichLog(id="messages", markup=True)
        yield Input(placeholder="Type a message...", id="message_input")

    def on_input_submitted(self, event: Input.Submitted):
        log = self.query_one("#messages", RichLog)
        log.write(f"[{self.color}]{self.user}[/{self.color}] > {event.value}")
        event.input.clear()


class LaternApp(App):
    def on_mount(self):
        self.push_screen(HomeScreen())

if __name__ == "__main__":
    LaternApp().run()
