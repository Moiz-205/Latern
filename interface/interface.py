from textual.app import App, ComposeResult
from textual.widgets import Input, Button, RichLog
from textual.screen import Screen

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Username", id="username")
        yield Input(placeholder="Color", id="color")
        yield Input(placeholder="Room Code", id="room_code")
        yield Button("Host", id="host")
        yield Button("Join", id="join")

class ChatScreen(Screen):
    def compose(self) -> ComposeResult:
        yield RichLog(id="messages")
        yield Input(placeholder="Type a message...", id="message_input")

class LaternApp(App):
    def on_mount(self):
        self.push_screen(HomeScreen())
