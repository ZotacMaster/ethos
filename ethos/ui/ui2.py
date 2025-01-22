from textual import work
from textual.app import App, ComposeResult
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from textual.widget import Widget
from textual.widgets import Input
from textual.reactive import reactive
from datetime import datetime

from ethos.utils import get_audio_url, fetch_tracks_list
from ethos.player import MusicPlayer
from ethos.tools import helper
from ethos.ui import assets

class Clock:
    """Renders the time in the center of the screen."""

    def __rich__(self) -> Text:
        return Text(datetime.now().ctime(), style="bold magenta", justify="center")



class RichLayout(Widget):
    """Rich Widget for ethos UI"""

    ASSETS = assets.UIAssets()
    layout = reactive(Layout)
    current_song = reactive("")
    is_player_playing = reactive(False)
    logs = reactive("")
    queue = reactive("")
    dashboard_data = reactive("")


    def on_mount(self) -> None:
        """Initialize the layout when the widget is mounted"""

        self.layout = Layout()
        self.layout.split(
            Layout(name="header", size=1),
            Layout(ratio=1, name="main"),
            Layout(size=7, name="player"),
        )
        self.layout.box = False

        self.layout["main"].split_row(Layout(name="side", ratio=2), Layout(name="cat", ratio=1))
        self.layout["side"].split(Layout(name="branding", size=7), Layout(name="playlists"))
        self.layout["player"].split_row(Layout(name="song_info", ratio=1), Layout(name="buttons", ratio=2))
    

    def update_layout(self):
        """Make the layout for app dashboard"""

        
        self.layout["cat"].update(
            Align.center(
                Text(
                    self.ASSETS.CAT_SYMBOL,
                    style="bold magenta",
                    justify="default"
                ),
                vertical="middle",
            )
        )

        self.layout["branding"].update(
            Align.center(
                Text(
                    self.ASSETS.BRANDING,
                    style="bold magenta",
                    justify="center"
                ),
                vertical="middle",
            )
        )

        self.layout["playlists"].update(
            Panel(
            Align.center(
                Text("Your Queue is empty"),
                vertical="top",
            ),
            box=False,
            border_style="blue"
            )
        )

        self.layout["header"].update(Clock())
        self.layout["buttons"].update(
            Panel(
                Align.center(
                    Text(self.ASSETS.BUTTON_SYMBOLS["playing"] if self.is_player_playing else self.ASSETS.BUTTON_SYMBOLS["paused"],
                    style="bold green",
                    justify="center"),
                    vertical="middle"
                )
            )
        )
        self.layout["song_info"].update(
            Panel(
                Align.center(
                    Text(f"{self.current_song}",
                         style="bold blue"),
                    vertical="middle"
                ),
            )
        )
        self.layout["playlists"].update(
            Panel(
                Align.center(
                    Text(
                        self.dashboard_data,
                        style="bold white",
                        justify="default"
                    ),
                ),
                border_style="none"
            )
        )
        
    def update_track(self, track_name: str) -> None:
        """Update the current playing song"""
        self.current_song = track_name
        self.is_player_playing = True
        self.refresh()
    

    def update_playing_status(self) -> None:
        """Update playing status of the player to render the controller buttons"""
        if self.is_player_playing:
            self.is_player_playing = False
        else:
            self.is_player_playing = True
        self.refresh()


    def update_dashboard(self, data: any) -> None:
        """Dynamically update dashboard data based on user interactions"""
        if type(data) == list:
            self.dashboard_data = "\n[bold red]Search Results:[/bold red]\n\n"+"\n".join(data) + "\n[bold red]Type track number to play[/bold red]"
            self.refresh()
        if type(data) == str:
            self.dashboard_data = data
            self.refresh()
                    

    def render(self) -> Layout:
        """Render the widget"""

        self.update_layout()
        return self.layout

        

class TextualApp(App):
    """Textual Application Class for ethos UI"""

    CSS_PATH = "./styles.tcss"

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+m", "pause", "Pause"),
        ("ctrl+r", "resume", "Resume"),
        ("ctrl+1", "volume_up"),
        ("ctrl+2", "volume_down")
    ]

    player = MusicPlayer()
    tracks_list = reactive([])
    track_to_play = reactive("")
    helper = helper.Format()

    def compose(self) -> ComposeResult:
        """Composer function for textual app"""

        yield RichLayout(id="rich-layout-widget")
        yield Input(placeholder="Type a command")


    def on_mount(self):
        """Handle functions after mounting the app"""

        self.input = reactive("")


    async def on_input_submitted(self, event: Input.Submitted):
        """Handle input submission"""

        layout_widget = self.query_one(RichLayout)
        if event.value:
            if event.value.startswith("/play"):
                search_track = self.helper.parse_command(event.value)
                self.tracks_list = await fetch_tracks_list(search_track)
                if self.tracks_list:
                    layout_widget.update_dashboard(self.tracks_list)
                    self.update_input()

            if event.value.isdigit() and self.tracks_list:
                self.track_to_play = self.tracks_list[int(event.value)-1]
                self.handle_play(self.track_to_play)
                self.update_input()

            if event.value.startswith("/volume"):
                volume_to_be_set = self.helper.parse_command(event.value)
                self.player.set_volume(volume_to_be_set)
                self.update_input()



    def action_pause(self):
        """Pause the player"""
        layout_widget = self.query_one(RichLayout)
        self.player.pause()
        layout_widget.update_playing_status()


    def action_resume(self):
        """Resume the player"""
        layout_widget = self.query_one(RichLayout)
        self.player.resume()
        layout_widget.update_playing_status()

    def action_volume_up(self):
        """Increase the volume by 5 levels"""
        current_volume = self.player.get_volume()
        self.player.set_volume(current_volume+5)

    def action_volume_down(self):
        """Decrease the volume by 5 levels"""
        current_volume = self.player.get_volume()
        self.player.set_volume(current_volume-5)

    def handle_play(self, track_name: str):
        """Function to handle the track playback"""
        layout_widget = self.query_one(RichLayout)
        url = get_audio_url(track_name+" official audio")
        self.player.set_volume(50)
        self.player.play(url)
        layout_widget.update_track(track_name)

    def update_input(self) -> None:
        """Function to reset the data in input widget once user enters his input"""
        input_widget = self.query_one(Input)
        input_widget.placeholder = ""
        input_widget.value = ""


    
if __name__ == "__main__":
    app = TextualApp()
    app.run()    
    