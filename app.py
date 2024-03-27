"""
Primary module for Froggit

This module contains the main controller class for the Froggit application. There
is no need for any additional classes in this module.  If you need more classes, 99%
of the time they belong in either the lanes module or the models module. If you are
unsure about where a new class should go, post a question on Piazza.

Alice Ke alk248
21.12.2020
"""
from consts import *
from game2d import *
from level import *
import introcs

from kivy.logger import Logger


# PRIMARY RULE: Froggit can only access attributes in level.py via getters/setters
# Froggit is NOT allowed to access anything in lanes.py or models.py.


class Froggit(GameApp):
    """
    The primary controller class for the Froggit application

    This class extends GameApp and implements the various methods necessary for
    processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Level object

        Method draw displays the Level object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Level.
    Level should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is managing the game state: when is the
    game started, paused, completed, etc. It keeps track of that in a hidden
    attribute

    Attribute view: The game view, used in drawing (see examples from class)
    Invariant: view is an instance of GView and is inherited from GameApp

    Attribute input: The user input, used to control the frog and change state
    Invariant: input is an instance of GInput and is inherited from GameApp
    """
    # HIDDEN ATTRIBUTES
    # Attribute _state: The current state of the game (taken from consts.py)
    # Invariant: _state is one of STATE_INACTIVE, STATE_LOADING, STATE_PAUSED,
    #            STATE_ACTIVE, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _level: The subcontroller for a  level, managing the frog and
    #obstacles
    # Invariant: _level is a Level object or None if no level is currently active
    #
    # Attribute _title: The title of the game
    # Invariant: _title is a GLabel, or None if there is no title to display
    #
    # Attribute _text: A message to display to the player
    # Invariant: _text is a GLabel, or None if there is no message to display

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _last: A bool for if s was pressed last frame
    # Invariant: _last is a bool

    #Attribute _last: The last key press
    #Invariant: _last is an int either 1 or 0.

    #Attribute _Pausetext: A message to display to the player
    #Invariant: _Pausetext is a GLabel, or None if there is no message to display

    #Attribute _Losetext: A message to display to the player
    #Invariant: _Losetext is a GLabel, or None if there is no message to display

    #Attribute _Wintext: A message to display to the player
    #Invariant: _Wintext is a GLabel, or None if there is no message to display

    #Attribute _hitbox: The contents of the loaded 'objects.json' file
    #Invariant: _hitbox is a nested dictionary

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        creates both the title (in attribute _title) and a message (in attribute
        _text) saying that the user should press a key to play a game.
        """
        self._state = STATE_INACTIVE
        self._level = None
        self._title = GLabel(text = "Froggit", font_name = ALLOY_FONT, \
        font_size = ALLOY_LARGE, linecolor = 'dark green', x = self.width//2, \
        bottom = self.height//2)
        self._text = GLabel(text = "Press 's' to start", font_name = ALLOY_FONT,\
        font_size = ALLOY_MEDIUM, x = self.width//2, top = self._title.bottom)
        self._last = 0
        self._Pausetext = GLabel(text = "Press 'c' to continue", font_size = \
            ALLOY_SMALL,font_name = ALLOY_FONT, x = 0, y = 0, fillcolor = \
            'forest green', linecolor = 'white')
        self._Losetext = GLabel(text = "You Lose!", font_size = \
            ALLOY_SMALL,font_name = ALLOY_FONT, x = 0, y = 0, fillcolor = \
            'forest green', linecolor = 'white')
        self._Wintext = GLabel(text = "You Win!", font_size = \
            ALLOY_SMALL,font_name = ALLOY_FONT, x = 0, y = 0, fillcolor = \
            'forest green', linecolor = 'white')
        self._Pausetext.width = self.width
        self._Pausetext.height = GRID_SIZE

    def update(self,dt):
        """
        Updates the game objects each frame.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Level. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Level object _level to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_LOADING, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays the title and a simple message on the screen. The application
        remains in this state so long as the player never presses a key.

        STATE_LOADING: This is the state that creates a new level and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame (the amount of time to load
        the data from the file) before switching to STATE_ACTIVE. One of the
        key things about this state is that it resizes the window to match the
        level file.

        STATE_ACTIVE: This is a session of normal gameplay. The player can
        move the frog towards the exit, and the game will move all obstacles
        (cars and logs) about the screen. All of this should be handled inside
        of class Level (NOT in this class).  Hence the Level class should have
        an update() method, just like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the frog after it was either killed
        or reached safety. The application switches to this state if the state
        was STATE_PAUSED in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over (all lives are lost or all frogs are safe),
        and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._determineState()
        self._isSTATE_LOADING()
        self._determineContinue()
        self._isSTATE_CONTINUE()

        if self._state == STATE_ACTIVE:
            self._text = None
            self._level.update(self.input, dt, self.view)
        elif self._state in [STATE_LOADING,STATE_PAUSED,STATE_CONTINUE,\
        STATE_COMPLETE]:
            self._title = None
        if not self._level is None and not self._state == STATE_PAUSED:
            if self._level.getFinished():
                if self._level.noLivesLeft():
                    self._gameLose()
                else:
                    self._state = STATE_PAUSED
                    self._Pausetext.x = self.width/2
                    self._Pausetext.y = (self.height-GRID_SIZE)/2
            if self._level.getWin():
                self._gameWin()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject. To draw a
        GObject g, simply use the method g.draw(self.view). It is that easy!

        Many of the GObjects (such as the cars, logs, and exits) are attributes
        in either Level or Lane. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        those two classes.  We suggest the latter.  See the example subcontroller.py
        from the lesson videos.
        """
        if not (self._title is None) and not (self._text is None):
            self._title.draw(self.view)
            self._text.draw(self.view)
        elif self._title is None and not self._text is None:
            self._text.draw(self.view)
        elif self._text is None and not self._title is None:
            self._title.draw(self.view)
        if not (self._level is None):
            self._level.draw(self.view)
        if self._state is STATE_PAUSED and not self._level.noLivesLeft():
            self._Pausetext.draw(self.view)
        if self._state == STATE_COMPLETE and self._level.noLivesLeft():
            self._Losetext.draw(self.view)
        if self._state == STATE_COMPLETE and self._level.getWin():
            self._Wintext.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def _determineState(self):
        """
        Takes input for the first screen and checks user input. If conditions
        are satisfied (i.e user presses 's'), state is changed to STATE_LOADING.

        Dismisses the welcome screen when user presses down the 'S' key.
        """
        if self._state == STATE_INACTIVE:
            # Determine the current number of keys pressed
            curr_keys = self.input.is_key_down('s')

            # Only change if we have just pressed the keys this animation frame
            press = curr_keys > 0 and self._last == 0

            if press:
                self._state = STATE_LOADING
                self._title = None
                self._text = None

            # Update last_keys
            self._last = curr_keys

    def _determineContinue(self):
        """
        Takes user input and checks if 'c' is pressed down. Resets the play
        mode after the game is paused.
        """
        if self._state is STATE_PAUSED and not self._level.noLivesLeft():
            curr_keys = self.input.is_key_down('c')

            # Only change if we have just pressed the keys this animation frame
            press = curr_keys > 0 and self._last == 0

            if press:
                self._level.makeFrog(self._hitbox)
                self._state = STATE_CONTINUE
                self._title = None
                self._text = None

            # Update last_keys
            self._last = curr_keys

    def _isSTATE_CONTINUE(self):
        """
        Ensures that STATE_CONTINUE only lasts one animation frame. This will
        change the state.
        """
        if self._state == STATE_CONTINUE:
            self._level.setFinished(False)
            self._state = STATE_ACTIVE

    def _isSTATE_LOADING(self):
        """
        Checks if the state is STATE_LOADING.

        If state is STATE_LOADING, load jsons and resize view window.
        """
        if self._state == STATE_LOADING:
            new_dict = self.load_json(DEFAULT_LEVEL)
            hitbox = self.load_json('objects.json')
            self._hitbox = hitbox
            values = new_dict['size']
            self.width = values[0] * GRID_SIZE
            self.height = (values[1]+1) * GRID_SIZE
            self._level = Level(new_dict, self._hitbox)
            self._state = STATE_ACTIVE

    def _gameLose(self):
        """
        Switches self._state to STATE_COMPLETE. If there are no lives left
        on the lives counter, the 'You lose' game screen is displayed.
        """
        if self._level.noLivesLeft():
            self._state = STATE_COMPLETE
            self._Losetext.x = self.width/2
            self._Losetext.y = (self.height-GRID_SIZE)/2
            self._Losetext.width = self.width
            self._Losetext.height = GRID_SIZE

    def _gameWin(self):
        """
        Switches state to STATE_COMPLETE and set x and y values for the win
        GLabel. If the game is complete (all exits are filled with safe frogs),
        the 'You win' screen will be shown.
        """
        self._state = STATE_COMPLETE
        self._Wintext.x = self.width/2
        self._Wintext.y = (self.height-GRID_SIZE)/2
        self._Wintext.width = self.width
        self._Wintext.height = GRID_SIZE
