
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


class Clock:
    """Renders the time in the center of the screen."""

    def __rich__(self) -> Text:
        return Text(datetime.now().ctime(), style="bold magenta", justify="center")



class RichLayout(Widget):
    """Rich Widget for ethos UI"""


    layout = reactive(Layout)

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
        """
        with Live(self.layout, screen=True, redirect_stderr=False):
            try:
                while True:
                    sleep(1)
            except KeyboardInterrupt:
                pass
        """


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
        ("ctrl+q", "quit", "Quit")
    ]

    def compose(self) -> ComposeResult:
        """Composer function for textual app"""

        yield RichLayout(id="rich-layout-widget")
        yield Input(placeholder="Type a command")


    def on_mount(self):
        """Handle functions after mounting the app"""

        self.input = reactive("")


    def on_input_submitted(self, event: Input.Submitted):
        """Handle input submission"""

        self.input = event.value


    
if __name__ == "__main__":
    app = TextualApp()
    app.run()    
    


    