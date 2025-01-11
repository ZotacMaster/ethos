from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button, Label
from textual.containers import Horizontal, Vertical, Container
from textual.reactive import var
from helper_functions import resolve_playlists, resolve_recents

class EthosMusicCLI(App):
    """UI for ethos music player"""

    CSS_PATH = "./ui.tcss"

    search = var("")
    queue = var([])
    now_playing = var(None)
    time_stamp = var(0)

    playlist_path = "../userfiles/playlists"
    recents_path = "../userfiles/recents.json"
    playlists = resolve_playlists(playlist_path)
    recents = resolve_recents(recents_path)
    
    def compose(self) -> ComposeResult:

        """
        DOM Structure:
        Horizontal
            Vertical
                Hero Section
                Playlists
            Vertical
                Search
                Recents
                Player
        """
        
        yield Header()
        yield Footer()

        branding = '''   ▄████████     ███        ▄█    █▄     ▄██████▄     ▄████████ 
  ███    ███ ▀█████████▄   ███    ███   ███    ███   ███    ███ 
  ███    █▀     ▀███▀▀██   ███    ███   ███    ███   ███    █▀  
 ▄███▄▄▄         ███   ▀  ▄███▄▄▄▄███▄▄ ███    ███   ███        
▀▀███▀▀▀         ███     ▀▀███▀▀▀▀███▀  ███    ███ ▀███████████ 
  ███    █▄      ███       ███    ███   ███    ███          ███ 
  ███    ███     ███       ███    ███   ███    ███    ▄█    ███ 
  ██████████    ▄████▀     ███    █▀     ▀██████▀   ▄████████▀  
                                                                '''
        
        subtitle = '''music-cli for cool folks'''
        guitar = """                          ,     
                      ,   |     
   _,,._              |  0'     
 ,'     `.__,--.     0'         
/   .--.        |           ,,, 
| [=========|==|==|=|==|=|==___]
\   "--"  __    |           ''' 
 `._   _,'  `--'                
    ""'     ,   ,0     ,        
hjm         |)  |)   ,'|        
  ____     0'   '   | 0'        
  |  |             0'           
 0' 0'"""
        #art - Guitar by Harry Mason

        is_recent = "You have not played any song recently" if not self.recents else True
        
        yield Horizontal(
            Vertical(
                Static(branding, classes="title"),
                Static(subtitle, classes="sub_title"),
                Container(
                    Static("[@click='app.bell']Your playlists[/]", classes="playlist_title"),
                    Button("Create Playlist [0]", variant='default', classes="playlist_button"),   
                )
            ),
            Vertical(
                Input(placeholder="Search music\t[s]", type="text", value=self.search, classes="search"),
                Container(
                    Static("Recents", classes="recents_title"),
                    Label(is_recent, classes="recents_body"),
                    id="recents"
                ),
                Static("Player", classes="player")
            ),
        )

    def on_mount(self) -> None:
        self.title = "ethos"
        self.sub_title = "music cli"
        self.screen.styles.background = "black"
        self.screen.styles.border = ("heavy", "green")

if __name__ == "__main__":
    app = EthosMusicCLI()
    app.run()
