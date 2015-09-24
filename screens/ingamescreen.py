from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.properties import NumericProperty
from screens import screenmanager
import random

__author__ = 'ohaz'

Builder.load_file('./screens/ingamescreen.kv')

# ----------------
# Global Variables
# ----------------

# This one should probably not be a global variable. Bad Design?
last_button = None

# A list of colours to use. Each element is a list of 2 colours - the lit one and a darker version of it.
colours = [['#FF0000', '#CC0000'], ['#FF00FF', '#CC00CC'], ['#0000FF', '#0000CC'], ['#00FF00', '#00CC00'],
           ['#FFFF00', '#CCCC00']]


class GameOverPopup(Popup):
    """
    The popup that appears if you either leave the game, or lose
    """

    def __init__(self, screen):
        """
        Initialise the popup
        :param screen: the screen the popup belongs to
        :return:
        """
        self.screen = screen
        super(GameOverPopup, self).__init__()

    def close(self):
        """
        Closes the popup. Also switches to the main menu
        :return:
        """
        self.dismiss()
        screenmanager.change_to('main_menu')


class ColourToggleButton(ToggleButton):
    """
    Use a toggle button as a way to display the coloured blocks.
    """

    def __init__(self, screen):
        """
        Initialise the Button
        :param screen: the screen this button belongs to
        :return:
        """
        super(ColourToggleButton, self).__init__()
        self.screen = screen
        self.visited = False

    def colour_press(self):
        """
        Event that gets fired when a button is pressed.
        :return:
        """
        global last_button
        if last_button is None:
            # If there is no "last button press", set this as the latest one
            last_button = self
        else:
            # Another button has been pressed before. Switch the colours of the two
            last_button.background_color, self.background_color = self.background_color, last_button.background_color
            # Set their states back to normal and reset the last button pressed
            last_button.state = 'normal'
            self.state = 'normal'
            last_button = None
            # Check if the switch removed any blocks
            points = self.screen.check_removal()
            if points == 0:
                # If nothing has been removed, the player gets one step closer to losing
                self.screen.misses += 1
            else:
                # Give the player the points
                self.screen.points += points
            if self.screen.misses > 3:
                # Player has lost, leave the game
                self.screen.leave()


class IngameScreen(Screen):
    """
    Class for the Ingame Screen.
    Contains a few labels for the points and the misses, the game itself and a leave button.
    """

    # Properties for the wrong moves the player did and the points.
    misses = NumericProperty(0)
    points = NumericProperty(0)

    def on_enter(self, *args):
        """
        Event that gets fired when the player enters this screen.
        Does cleanup from previous games and prepares the new game
        :param args: arguments passed
        :return:
        """
        # Set the wrong moves and the points to 0
        self.misses = 0
        self.points = 0
        # Create a new random seed for colour generation
        random.seed()
        # Clear the grid from previous games
        grid = self.ids.grid
        grid.clear_widgets()
        for i in range(0, grid.rows * grid.cols):
            # Create new Coloured Buttons with random colours from the colours list
            c_button = ColourToggleButton(self)
            colour = random.randint(0, len(colours)-1)
            c_button.background_color = get_color_from_hex(colours[colour][0])
            grid.add_widget(c_button)

    def check_removal(self, multiplier=1):
        """
        Recursive function that checks if enough blocks with the same colour are next to each other
        :param multiplier: The point multiplier
        :return: Points the player gets for this step
        """
        children = self.ids.grid.children
        groups = []
        points = 0

        # Recursively check all children and creates groups with them
        for i, child in enumerate(children):
            if not child.visited:
                groups.append(self.recursive_check(i))

        # Reset visit status for the next pass
        for child in children:
            child.visited = False

        # Get the groups that contain more than 3 blocks of the same colour, calculate points and let new blocks fall
        high_groups = [x for x in groups if len(x) > 3]
        for g in high_groups:
            # I sort the blocks by reversed id, this helps in the implementation of how blocks fall
            # If this was unsorted, a block might get the colour of the block above that actually should get removed
            g.sort(reverse=True)
            points += multiplier * len(g)
            multiplier += 1
            for button_id in g:
                self.fall(button_id)
        if len(high_groups) > 0:
            return self.check_removal(multiplier) + points
        else:
            return 0

    def fall(self, current):
        """
        Gravity implementation. Blocks fall down (also spawns new ones)
        :param current: the block we are currently visiting
        :return:
        """
        grid = self.ids.grid
        children = grid.children

        # The block above the current one is the one with the higher id
        child_above = current + grid.cols

        # the top row of blocks starts with this id
        topmost = len(grid.children) - grid.cols

        if child_above > topmost:
            # We are in the top row, generate new coloured block
            colour = random.randint(0, len(colours)-1)
            children[current].background_color = get_color_from_hex(colours[colour][0])
        else:
            # Let the block on top of us fall down and do the same for the block above
            children[current].background_color = children[child_above].background_color
            self.fall(child_above)

    def recursive_check(self, current):
        """
        Recursively check the blocks for groups
        :param current: the block currently visited
        :return: a list of blocks
        """
        grid = self.ids.grid
        children = grid.children
        own_color = children[current].background_color
        children[current].visited = True
        own_list = [current]

        # Get all children next to the current one
        child_top = current - grid.cols
        if child_top < 0:
            child_top = None
        child_bot = current + grid.cols
        if child_bot >= grid.rows * grid.cols:
            child_bot = None
        child_left = None
        child_right = None
        if current % grid.cols > 0:
            child_left = current - 1
        if current % grid.cols < grid.cols - 1:
            child_right = current + 1
        children_next = [child_top, child_bot, child_left, child_right]

        # Check if children need to get added to the list
        for child in children_next:
            if child is not None:
                if children[child].background_color == own_color and not children[child].visited:
                    own_list.extend(self.recursive_check(child))

        return own_list

    def leave(self):
        """
        Leave the game. Creates a popup that shows the score
        :return:
        """
        p = GameOverPopup(self)
        p.open()
