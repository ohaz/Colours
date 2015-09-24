# -*- coding: utf-8 -*-

# Main kivy import
import kivy

# Additional kivy imports
from kivy.app import App
from kivy.config import Config

# Screens
from screens import screenmanager
from screens.mainscreen import MainScreen
from screens.ingamescreen import IngameScreen

# Cause program to end if the required kivy version is not installed
kivy.require('1.8.0')

__author__ = 'ohaz'

# ---------------
# Config settings
# ---------------

# Multitouch emulation creates red dots on the screen. We don't need multitouch, so we disable it
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# ---------------------
# Local initialisations
# ---------------------

# Initialise the screen manager (screens/screenmanager.py)
screenmanager.init()

# Add the two screens to it
screenmanager.set_screens([MainScreen(name='main_menu'), IngameScreen(name='ingame')])

# Start with the main menu screen
screenmanager.change_to('main_menu')


class ColoursApp(App):
    """
    The main Class.
    Only needed for the build function.
    """
    def build(self):
        """
        Method to build the app.
        :return: the screenmanager
        """
        return screenmanager.get_sm()

# Create the app and run it
if __name__ == '__main__':
    ColoursApp().run()
