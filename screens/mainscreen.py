from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from screens import screenmanager
from kivy.app import App

__author__ = 'ohaz'

# Load the fitting kv file
Builder.load_file('./screens/mainscreen.kv')


class MainScreen(Screen):
    """
    The main screen. Has a play and a quit button.
    A highscore Button might be added in the future
    """

    def start_game(self):
        """
        Starts the game by switching to the ingame screen
        :return:
        """
        screenmanager.change_to('ingame')

    def leave_game(self):
        """
        Ends the game by stopping the app
        :return:
        """
        # Exit the application, clean up
        App.get_running_app().stop()
