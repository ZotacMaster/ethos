
"""
Entry point of the application
"""


import os
import sys
import dotenv
sys.path.append(os.getcwd())

from ethos.ui import ui

def main():
    dotenv.load_dotenv()
    ethos_ui = ui.UI()
    ethos_ui.draw_ui()
