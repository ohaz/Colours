from kivy.uix.screenmanager import ScreenManager, SlideTransition

__author__ = 'ohaz'

# -----------------------------------------------
# Variables for the screenmanager and the screens
# -----------------------------------------------

screen_manager = None
screens = None


def init():
    """
    Creates a new Screenmanager and initialises settings
    :return:
    """
    global screen_manager
    screen_manager = ScreenManager(transition=SlideTransition())


def set_screens(screen_list):
    """
    Sets the list of screens for use in the screenmanager
    :param screen_list: a list of Screen Objects
    :return:
    """
    global screens, screen_manager
    screens = screen_list
    for s in screen_list:
        screen_manager.add_widget(s)


def get_sm():
    """
    Gets the screenmanager
    :return: The screenmanager
    """
    global screen_manager
    return screen_manager


def change_to(name):
    """
    A function that internally uses the current variable to change the screen
    :param name: the name of the screen to switch to
    :return:
    """
    global screen_manager
    screen_manager.current = name

