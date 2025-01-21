
from textual.app import App, ComposeResult
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from textual.widget import Widget
from textual.widgets import Input
from textual.reactive import reactive
from datetime import datetime
from time import sleep

from ethos.utils import get_audio_url, fetch_tracks_list
from ethos.player import MusicPlayer

class Clock:
    """Renders the time in the center of the screen."""

    def __rich__(self) -> Text:
        return Text(datetime.now().ctime(), style="bold magenta", justify="center")



class RichLayout(Widget):
    """Rich Widget for ethos UI"""


    layout = reactive(Layout)
    current_song = reactive("")
    is_player_playing = reactive(False)
    button_symbols_playing = reactive("↻      ◁     ||     ▷       ↺")
    button_symbols_paused = reactive("↻      ◁     ▷     ▷       ↺")
    logs = reactive("")


    def on_mount(self) -> None:
        """Initialize the layout when the widget is mounted"""

        self.branding = """        __  .__                  
  _____/  |_|  |__   ____  ______
_/ __ \   __\  |  \ /  _ \/  ___/
\  ___/|  | |   Y  (  <_> )___ \ 
 \___  >__| |___|  /\____/____  >
     \/          \/           \/ """
    
    
        self.cat_symbol = """                                                            
                                                            
                                                            
                                    :=*=                    
                                  .*#-.#=                   
                          .-+*#%%%%%*+-+#                   
                 .=+***++#@@@@@@@@@@@@@@%.                  
                 %#:.:#@@@@@@@@@@@@@@@@@@%=                 
                 *#.=%@@@@@@@@@@@@+=+#@@@@%+                
                  #%@@@@@%#*#@@@@@%@@@@@@%%%=               
                   %%%@@%++*%@%#%@@@@@@%%%%%=               
                  .@@%%%@@@@@@#-#@@%%%%%%%@*                
                   %@@@%%%@@@%#= .*%%%%%@@*.                
                   =@@@@@%%%@@@#--%@@@@@#-                  
                    =*%@@@@%%@@@@@@@@%%%.                   
                      .:-*@@@@@@@@@@@@@@-                   
              :**+       =@@@@@@%@@@@@@@-                   
             *#.        .%@@@@@@@%%%@@@@:                   
            =%         .#@@@@@@@@@@%%%@#                    
            +%.       .#%@@@@@@@@@@@@%%*                    
            .%#:     .*%@@@@@#@@%#@@@@@%=                   
             .+%#++*%%@@@#@@@##@*%@@@#@@-                   
                .----.-%@+#@@%=@+@@@*%%=                    
                  ....:-*=:***===**+=*=:....                
"""

        self.layout = Layout()
        self.layout.split(
            Layout(name="header", size=1),
            Layout(ratio=1, name="main"),
            Layout(size=10, name="player"),
        )

        self.layout["main"].split_row(Layout(name="side", ratio=2), Layout(name="cat", ratio=1))
        self.layout["side"].split(Layout(name="branding", size=7), Layout(name="playlists"))
        self.layout["player"].split_row(Layout(name="song_info", ratio=1), Layout(name="buttons", ratio=2))
    

    def update_layout(self):
        """Make the layout for app dashboard"""

        
        self.layout["cat"].update(
            Align.center(
                Text(
                    self.cat_symbol,
                    style="bold magenta",
                    justify="default"
                ),
                vertical="middle",
            )
        )

        self.layout["branding"].update(
            Align.center(
                Text(
                    self.branding,
                    style="bold magenta",
                    justify="center"
                ),
                vertical="middle",
            )
        )

        self.layout["playlists"].update(
            Panel(
            Align.center(
                Text("Your Playlists"),
                vertical="top",
            ),
            border_style="blue"
            )
        )

        self.layout["header"].update(Clock())
        self.layout["buttons"].update(
            Panel(
                Align.center(
                    Text(self.button_symbols_playing if self.is_player_playing else self.button_symbols_paused,
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
                )
            )
        )
        self.layout["playlists"].update(
            Panel(
                Align.center(
                    Text(
                        self.logs,
                        style="bold white",
                        justify="default"
                    ),
                )
            )
        )
        
    def update_track(self, track_name: str) -> None:

        self.current_song = track_name
        self.is_player_playing = True
        self.refresh()
    

    def update_playing_status(self) -> None:

        if self.is_player_playing:
            self.is_player_playing = False
        else:
            self.is_player_playing = True

        self.refresh()

    def update_logs(self, message: str) -> None:
        self.logs = self.logs + "\n" + message
        self.refresh()
    

    def update_clock(self) -> None:    
        with Live(self.layout, screen=True, redirect_stderr=False):
            try:
                while True:
                    sleep(1)
            except KeyboardInterrupt:
                pass
        


    def render(self) -> Layout:
        """Render the widget"""

        self.update_layout()
        return self.layout

        

class TextualApp(App):
    """Textual Application Class for ethos UI"""

    CSS = """
    #rich-layout-widget {
        height: 100%;
    }

    Input {
        dock: bottom;
    }
    """

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+m", "pause", "Pause"),
        ("ctrl+r", "resume", "Resume"),
        ("ctrl+1", "volume_up"),
        ("ctrl+2", "volume_down")
    ]

    player = MusicPlayer()

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
        tracks_list = await fetch_tracks_list(event.value)
        track_name = tracks_list[0]
        url = get_audio_url(track_name)
        self.player.play(url)
        layout_widget.update_logs(f"Playing {track_name}")
        layout_widget.update_track(track_name)
        


    def action_pause(self):
        """Pause the player"""
        layout_widget = self.query_one(RichLayout)
        self.player.pause()
        layout_widget.update_playing_status()
        layout_widget.update_logs("player paused")


    def action_resume(self):
        """Resume the player"""
        layout_widget = self.query_one(RichLayout)
        self.player.resume()
        layout_widget.update_playing_status()
        layout_widget.update_logs("player resumed")

    def action_volume_up(self):
        """Increase the volume by 5 levels"""
        current_volume = self.player.get_volume()
        self.player.set_volume(current_volume+5)
        layout_widget = self.query_one(RichLayout)
        layout_widget.update_logs(f"set volume {self.player.get_volume()}")

    def action_volume_down(self):
        """Decrease the volume by 5 levels"""
        current_volume = self.player.get_volume()
        self.player.set_volume(current_volume-5)
        layout_widget = self.query_one(RichLayout)
        layout_widget.update_logs(f"set volume {self.player.get_volume()}")


    
if __name__ == "__main__":
    app = TextualApp()
    app.run()    
    


    