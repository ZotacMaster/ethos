from textual.app import App, ComposeResult
from textual.widgets import Label, Header, Footer, Static
from textual.containers import Container

class EthosMusicCLI(App):

    CSS_PATH = "./ui.tcss"

    

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        s = '''   ▄████████     ███        ▄█    █▄     ▄██████▄     ▄████████ 
  ███    ███ ▀█████████▄   ███    ███   ███    ███   ███    ███ 
  ███    █▀     ▀███▀▀██   ███    ███   ███    ███   ███    █▀  
 ▄███▄▄▄         ███   ▀  ▄███▄▄▄▄███▄▄ ███    ███   ███        
▀▀███▀▀▀         ███     ▀▀███▀▀▀▀███▀  ███    ███ ▀███████████ 
  ███    █▄      ███       ███    ███   ███    ███          ███ 
  ███    ███     ███       ███    ███   ███    ███    ▄█    ███ 
  ██████████    ▄████▀     ███    █▀     ▀██████▀   ▄████████▀  
                                                                '''
        
        subtitle = '''               _         _ _    __                       _    __     _ _       
  _ __ _  _ __(_)__   __| (_)  / _|___ _ _   __ ___  ___| |  / _|___| | |__ ___
 | '  \ || (_-< / _| / _| | | |  _/ _ \ '_| / _/ _ \/ _ \ | |  _/ _ \ | / /(_-<
 |_|_|_\_,_/__/_\__| \__|_|_| |_| \___/_|   \__\___/\___/_| |_| \___/_|_\_\/__/
                                                                               '''
        
        #hero-section
        yield Container(
            Static(s, classes="title"),
            Static(subtitle, classes="sub_title"),
            id="hero"
        )
        #neko-section


    def on_mount(self) -> None:
        self.title = "ethos"
        self.sub_title = "music cli"
        self.screen.styles.background = "black"
        self.screen.styles.border = ("heavy", "green")

if __name__ == "__main__":
    app = EthosMusicCLI()
    app.run()
