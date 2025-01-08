from textual.app import App, ComposeResult
from textual.widgets import Label, Header, Footer, Static
from textual.containers import Container

class EthosMusicCLI(App):

    CSS_PATH = "./ui.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(
            Static("ethos", classes="title"),
            Static("music cli for cool folks", classes="sub_title"),
            id="hero"
        )

    def on_mount(self) -> None:
        self.title = "ethos"
        self.sub_title = "music cli"
        self.screen.styles.background = "black"
        self.screen.styles.border = ("heavy", "green")

if __name__ == "__main__":
    app = EthosMusicCLI()
    app.run()
