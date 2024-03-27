"""
Subcontroller module for Froggit

This module contains the subcontroller to manage a single level in the Froggit game.
Instances of Level represent a single game, read from a JSON.  Whenever you load a new
level, you are expected to make a new instance of this class.

The subcontroller Level manages the frog and all of the obstacles. However, those are
all defined in models.py.  The only thing in this class is the level class and all of
the individual lanes.

This module should not contain any more classes than Levels. If you need a new class,
it should either go in the lanes.py module or the models.py module.

Alice Ke alk248
21.12.2020
"""
from game2d import *
from consts import *
from lanes  import *
from models import *

import time

# PRIMARY RULE: Level can only access attributes in models.py or lanes.py using getters
# and setters. Level is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Level(object):
    """
    This class controls a single level of Froggit.

    This subcontroller has a reference to the frog and the individual lanes.  However,
    it does not directly store any information about the contents of a lane (e.g. the
    cars, logs, or other items in each lane). That information is stored inside of the
    individual lane objects.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lesson 27 for an example.  This class will be similar to that
    one in many ways.

    All attributes of this class are to be hidden.  No attribute should be accessed
    without going through a getter/setter first.  However, just because you have an
    attribute does not mean that you have to have a getter for it.  For example, the
    Froggit app probably never needs to access the attribute for the Frog object, so
    there is no need for a getter.

    The one thing you DO need a getter for is the width and height.  The width and height
    of a level is different than the default width and height and the window needs to
    resize to match.  That resizing is done in the Froggit app, and so it needs to access
    these values in the level.  The height value should include one extra grid square
    to suppose the number of lives meter.
    """
    pass
    # LIST ALL HIDDEN ATTRIBUTES HERE
    #Attribute _lanes: The list of lanes
    # Invariant: _lanes is a list of GTile objects

    #Attribute _frog: The frog object
    # Invariant: _frog is a object of class Frog

    #Attribute _jsonLanes: The list of lanes from the json.
    # Invariant: _jsonLanes is a list with nested dictionaries.

    #Attribute _fulljson: The full loaded json
    # Invariant: _fulljson is a nested dictionary.

    #Attribute _frogpos: The frog's intial position
    # Invariant: frog pos is a list of length 2 with ints stored inside

    #Attribute _title: The text for the Lives counter 'Lives: '
    # Invariant: _title is an instance of GLabel

    #Attribute _numsafeFrogs: The number that represents how many safe blug
    #frogs are on a lilypad
    # Invariant: _numsafeFrogs is an int

    #Attribute _deathAnimator: A coroutine for performing the death animation
    # Invariant: _deathAnimator is a generator-based coroutine (or None)

    #Attribute _deathPosition: The death sprite's position
    # Invariant: _deathPosition is a list of length 2 with only int or floats
    #within it

    #Attribute _finished: Indicates that the frog has died.
    # Invariant: _finished is a bool, either True or False.

    #Attribute _win: The flag for if all exits are full.
    # Invariant: _win is a bool, either True or False.

    #Attribute _lives: _lives stores the frog heads which are 'lives'
    # Invariant: _lives is None or a list of GImage objects

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getFrogX(self):
        """
        Returns the x position of the frog instance
        """
        return self._frog.x

    def getFrogY(self):
        """
        Returns the y position of the frog instance
        """
        return self._frog.y

    def setFrogX(self, x):
        """
        Sets the self._frog.x attribute to x
        """
        self._frog.x = x

    def setFrogY(self, y):
        """
        Sets the self._frog.y attribute to y
        """
        self._frog.y = y

    def getFrog(self):
        """
        Returns the frog object.
        """
        return self._frog

    def getLanesList(self):
        """
        Returns a list of Lane objects (Hedge, Road, Water or Grass).
        """
        return self._lanes

    def getFrogStart(self):
        """
        Returns the frog's position
        """
        return self._frogpos

    def getDeathAnimator(self):
        """
        Returns the death animator.
        """
        return self._deathAnimator

    def getFinished(self):
        """
        Returns the value (True or False) stored as self._finished.
        """
        return self._finished

    def setFinished(self, val):
        """
        Sets the value of the self._finished attribute to the given input val.

        Parameter val: val is the desired value to change the attribute to.
        Precondition: val is a bool either True or False.
        """
        self._finished = val

    def getWin(self):
        """
        Returns the value of self._win
        """
        return self._win

    # INITIALIZER (standard form) TO CREATE THE FROG AND LANES
    def __init__(self, json_dict, hitboxjson):
        """
        Initializes the background of the game at the start.

        Parameter json_dict: json_dict is the loaded json file for the level.
        Precondition: json_dict is a nested dictionary that is taken from the
        json loaded for the level.

        Parameter hitboxjson: hitboxjson is the loaded json file for the
        images and sprites which contain hitbox values.
        Precondition: hitboxjson is a loaded json file.
        """
        self._lanes = []
        lanes_list = json_dict['lanes']
        self._jsonLanes = lanes_list
        self._fulljson = json_dict
        width = json_dict['size'][0]*GRID_SIZE
        height = (json_dict['size'][1]+1)*GRID_SIZE
        self._initLanes(lanes_list,json_dict, hitboxjson)
        frog_pos = json_dict['start']
        self._frogpos = frog_pos
        self._livesCounter(w=width,h=height)
        self._cooldown = FROG_SPEED
        self._finished = False
        self._numsafeFrogs = 0
        self.makeFrog(hitboxjson)
        self._makeDeathSprite(hitboxjson)
        self._deathAnimator = None
        self._deathPosition = [-1000, 0]
        self._win = False

    # UPDATE METHOD TO MOVE THE FROG AND UPDATE ALL OF THE LANES
    def update(self, input, dt, view):
        """
        Moves the frog and updates all the lanes.

        This method controls the movement of the frog and checks if
        the frog has collided with an obstacle. It also checks if the frog
        starys within the bounds of the view window.

        Parameter input: The user input, used to control the frog and change
        state
        Precondition: input is an instance of GInput and is inherited from
        GameApp

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView and is inherited from GameApp
        """
        self._updateDeath(input, dt, view)
        if self._frog is not None:
            self._frogTurn(input)

            if 0>self._frog.y-GRID_SIZE and input.is_key_down('down'):
                return
            elif self._frog.y>(view.height-GRID_SIZE) and input.is_key_down('up'):
                return
            elif 0>self._frog.x-GRID_SIZE and input.is_key_down('left'):
                return
            elif self._frog.x>view.width-GRID_SIZE and input.is_key_down('right'):
                return

            self._moveFrog(input, dt, view)

            for lane in self.getLanesList():
                position = 0
                position +=1
                if isinstance(lane, Water) or isinstance(lane, Road):
                    lane.update(dt, self._fulljson)

            for lane in self.getLanesList():
                if lane.collides(self._frog):
                    if isinstance(lane, Hedge):
                        self._hedgeChecks(lane, input, dt, view)
                    else:
                        self._moveFrogBack(input, dt, view)
                        self._frog.update(input, dt, view)

                    if isinstance(lane, Road):
                        self._roadChecks(lane)

                    if isinstance(lane, Water):
                        self._waterChecks(lane, view, dt)
                    break;

    # DRAW METHOD TO DRAW THE FROG AND THE INDIVIDUAL LANES
    def draw(self, view):
        """
        Draws the game objects (lanes and frog) to the view.

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView and is inherited from GameApp
        """
        for lane in self._lanes:
            lane.draw(view)
        if not self._frog is None:
            self._frog.draw(view)
        for l in self._lives:
            l.draw(view)
        self._title.draw(view)
        self._deathSprite.draw(view)

    # ANY NECESSARY HELPERS (SHOULD BE HIDDEN)
    def noLivesLeft(self):
        """
        Returns True if the list of lives (counting the no. of frog heads left)
        is an empty list and False otherwise.
        """
        return self._lives == []

    def makeFrog(self,hitboxjson):
        """
        Creates a new frog object and sets the position to the inital start
        position.

        This method will create an instance of the Frog class and set its
        position to the start position of the frog when the game initially
        began.

        Parameter hitboxjson: hitboxjson is the loaded json file for the
        images and sprites which contain hitbox values.
        Precondition: hitboxjson is a loaded json file.
        """
        sprites_hitboxDict = hitboxjson['sprites']
        for val in sprites_hitboxDict:
            if val == 'frog':
                format = sprites_hitboxDict[val]['format']
                source = sprites_hitboxDict[val]["file"]
                hitboxes = sprites_hitboxDict[val]["hitboxes"]
        self._frog = Frog(x=self._frogpos[0], y=self._frogpos[1], format = \
        format,source = source,hitboxes=tuple(hitboxes), hitboxjson = \
        hitboxjson)

    def _hedgeChecks(self, lane, input, dt, view):
        """
        Completes all the hedge checks.

        Hedge checks are whether it is an exit or not, is there a safe frog
        on the exit, is movement allowed through the opening, blocking the
        hedge.

        Parameter lane:the lane that the frog is on.
        Precondition: lane is the lane object. lane is an instance from either
        Grass, Road, Hedge or Water class.

        Parameter input: The user input, used to control the frog and change
        state
        Precondition: input is an instance of GInput and is inherited from
        GameApp

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView and is inherited from GameApp
        """
        if lane.checkHedgeExit(self._frog):
            if lane.checkHedgeOpening(self._frog):
                self._moveFrogBack(input, dt, view)
                self._frog.update(input, dt, view)
            elif lane.blockExit(self._frog):
                self._moveFrogBack(input, dt, view)
            else:
                self._moveFrogBack(input, dt, view)
                self._frog.update(input, dt, view)
                self._frog.playExitSound()

            if lane.SafeHedgeExit(self._frog):
                self._finished = True
                self._frog = None
                self._numsafeFrogs += 1
        else:
            self._moveFrogBack(input, dt, view)

        if self._allExitsFull(lane):
            self._finished = True
            self._frog = None

    def _roadChecks(self, lane):
        """
        Checks if the car and frog have hit each other.

        This will check if a car and the frog have hit each other and if so, a
        death is lost, play the death sound,

        Parameter lane:the lane that the frog is on.
        Precondition: lane is the lane object. lane is an instance from either
        Grass, Road, Hedge or Water class.
        """
        if lane.checkCarCollision(self._frog):
            self._frog.playDeathSound()
            self._deathPosition = [self._frog.x, self._frog.y]
            self._frog = None
            self._frogDeathCountdown()
            return

    def _waterChecks(self, lane, view, dt):
        """
        Runs all the water checks on the frog when it is in a water lane.

        Water checks include whether the frog is on a log or not. If it is not
        on a log, then the frog dies. Also controls the frog death when the
        frog moves offscreen with the log.

        Parameter lane:the lane that the frog is on.
        Precondition: lane is the lane object. lane is an instance from either
        Grass, Road, Hedge or Water class.

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView and is inherited from GameApp

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        if self._frog.getAnimator() is None:
            lane.moveFrogwithLog(self._frog, lane, dt)
        if lane.checkWaterCollision(self._frog) and \
            self._frog.getAnimator() is None:
            self._frog.playDeathSound()
            self._deathPosition = [self._frog.x, self._frog.y]
            self._frog = None
            self._frogDeathCountdown()
            return
        self._offscreen(view.width)

    def _restrictBounds(self, view, input):
        """
        Prevents frog from moving off screen.

        This method restricts the frog to stay within the bounds of the view
        window by checking if the frog is trying to move offscreen.

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView and is inherited from GameApp

        Parameter input: The user input, used to control the frog and change
        state
        Precondition: input is an instance of GInput and is inherited from
        GameApp

        """
        if 0>self._frog.y-GRID_SIZE and input.is_key_down('down'):
            return
        elif self._frog.y>(view.height-GRID_SIZE) and input.is_key_down('up'):
            return
        elif 0>self._frog.x-GRID_SIZE and input.is_key_down('left'):
            return
        elif self._frog.x >view.width-GRID_SIZE and input.is_key_down('right'):
            return

    def _initLanes(self, lanes_list, json_dict, hitboxjson):
        """
        Creates the correct lane objects.

        This method is a helper to the intializer. It will create the lanes for
        the level as instances of the subclasses Hedge, Road, Grass or Water.

        Parameter lanes_list: The lane list from the full json loaded for the
        level.
        Precondition: lanes_list is a nested list with dictionaries inside.

        Parameter json_dict: json_dict is the loaded json file for the level.
        Precondition: json_dict is a nested dictionary that is taken from the
        json loaded for the level.

        Parameter hitboxjson: hitboxjson is the loaded json file for the
        images and sprites which contain hitbox values.
        Precondition: hitboxjson is a loaded json file.
        """
        for lane in range(len(lanes_list)):
            lane_type = lanes_list[lane]['type']
            if lane_type == "grass":
                lane_val = Grass(json_dict,lane, hitboxjson)
            elif lane_type == "road":
                lane_val = Road(json_dict,lane, hitboxjson)
            elif lane_type== "water":
                lane_val = Water(json_dict,lane, hitboxjson)
            elif lane_type=="hedge":
                lane_val = Hedge(json_dict,lane, hitboxjson)
            self._lanes.append(lane_val)

    def _offscreen(self, viewX):
        """
        Checks if the frog's center is within the view window.

        This function is called after the frog moves with the log. This will be
        called and if the frog is outside of the view window width bounds, the
        frog is 'killed', meaning a life is lost.

        Parameter: viewX is the window view width.
        Precondition: viewX is an int or float
        """
        if self._frog.x < 0 or self._frog.x > viewX:
            self._deathPosition = [self._frog.x, self._frog.y]
            self._frog.playDeathSound()
            self._frog = None
            self._frogDeathCountdown()

    def _updateDeath(self, input, dt, view):
        """
        Controls the death sprite.

        This method is part of enabling the death sprite to animate. It will
        control whether the death sprite animation is run.

        Parameter input: The user input, used to control the frog and change
        state
        Precondition: input is an instance of GInput

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView and is inherited from GameApp
        """
        if self._frog is None:
            if self._deathAnimator is not None:
                try:
                    self._deathAnimator.send(dt)
                except:
                    self._deathAnimator = None
            else:          # Stop animating
                self._deathSprite.x = self._deathPosition[0]
                self._deathSprite.y = self._deathPosition[1]
                self._deathAnimator = self._deathAnimation(dt)
                assert self._deathAnimator != None
                next(self._deathAnimator) # Start up the animator

    def _makeDeathSprite(self, hitboxjson):
        """
        Initializes the death sprite.

        This is a helper to the initializer. It will intialize the values for
        the death sprite.

        Parameter hitboxjson: hitboxjson is the loaded json file for the
        images and sprites which contain hitbox values.
        Precondition: hitboxjson is a loaded json file.
        """
        sprites_hitboxDict = hitboxjson['sprites']
        for val in sprites_hitboxDict:
            if val == 'skulls':
                format = sprites_hitboxDict[val]['format']
                source = sprites_hitboxDict[val]["file"]
        #make it a constant called offscreen
        self._deathSprite = GSprite(x=-1000, y=0, format = format,\
            source = source)
        self._deathSprite.frame = 0

    def _deathAnimation(self, dt):
        """
        Animates the death animation.

        A coroutine for performing the death animation. This will animate the
        death sprite once the frog has hit either a car or the water.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        currentTime = 0
        finalTime = DEATH_SPEED
        animating = True
        while animating:
            dt = (yield)
            currentTime += dt
            frac = currentTime/finalTime
            frame = DEATH_START + frac * DEATH_END
            self._deathSprite.frame = round(frame)
            if currentTime >= finalTime:
                self._deathSprite.x = -1000
                self._deathAnimator = None
                self._finished = True

    def _allExitsFull(self, lane):
        """
        Returns True if all exits have safe frogs on them. False otherwise.

        Checks if all exits are full. Exits are full if a safe frog is placed
        on all of the lilypads.

        Parameter lane:the lane that the frog is on.
        Precondition: lane is the lane object. lane is an instance from either
        Grass, Road, Hedge or Water class.
        """
        if self._numsafeFrogs == len(lane.getexitsOnly()):
            self._win = True
        return self._numsafeFrogs == len(lane.getexitsOnly())

    def _livesCounter(self, w, h):
        """
        Creates and positions the lives counter.

        This is a helper to the initialzer. This method will initialize the
        lives counter.

        Parameter w: width is width of the window view
        Precondition: w is an int or float

        Parameter h: height is the height of the windo view
        Precondition: h is an int or float
        """
        self._lives = []
        for l in range(3):
            life = GImage(width = GRID_SIZE, height = GRID_SIZE, source = \
            FROG_HEAD)
            life.x = w-GRID_SIZE/2
            life.y = h-GRID_SIZE/2
            if l>0:
                life.x= (life.x -(GRID_SIZE*l))
            self._lives.append(life)
        self._title = GLabel(text='Lives:',font_size = ALLOY_SMALL, \
        font_name = ALLOY_FONT)
        self._title.linecolor = 'forest green'
        self._title.y = h - GRID_SIZE/2
        self._title.x = w - GRID_SIZE*3
        self._title.right = self._lives[2].left

    def _frogDeathCountdown(self):
        """
        Removes a live each time the frog dies.

        This method detects if the frog has died or not and will remove a frog
        head from the lives counter if the frog has died.
        """
        if self._frog is None and not self._lives == []:
            del self._lives[0]

    def _frogTurn(self, input):
        """
        Sets angle when the frog turns direction when it moves.

        This method turns the frog in accordance to the user input. Depending on
        the direction (up, down, left, right), the frog will also turn to face
        that direction.

        Parameter input: The user input, used to control the frog and change
        state
        Precondition: input is an instance of GInput
        """
        if input.is_key_down('up'):
            self._frog.angle = FROG_NORTH
        if input.is_key_down('down'):
            self._frog.angle = FROG_SOUTH
        if input.is_key_down('left'):
            self._frog.angle = FROG_WEST
        if input.is_key_down('right'):
            self._frog.angle = FROG_EAST

    def _moveFrog(self, input, dt, view):
        """
        Moves the frog after a directional key is pressed.

        This method will move the frog based on the user input.

        Parameter input: The user input, used to control the frog and change
        state
        Precondition: input is an instance of GInput

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView and is inherited from GameApp
         """
        x = self.getFrogX()
        y = self.getFrogY()
        if input.is_key_down('left'):
            x=x-GRID_SIZE
            self._setFrogPosition(x,y,view,input)
        elif input.is_key_down('right'):
            x=x+GRID_SIZE
            self._setFrogPosition(x,y,view,input)
        elif input.is_key_down('up'):
            y=y+GRID_SIZE
            self._setFrogPosition(x,y,view,input)
        elif input.is_key_down('down'):
            y=y-GRID_SIZE
            self._setFrogPosition(x,y,view,input)

    def _moveFrogBack(self, input, dt, view):
        """
        Moves the frog back in the direction that the frog initially came from.

        This method will move the frog backwards.

        Parameter input: The user input, used to control the frog and change
        state
        Precondition: input is an instance of GInput

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView and is inherited from GameApp
        """
        x = self.getFrogX()
        y = self.getFrogY()
        if input.is_key_down('left'):
            x=x+GRID_SIZE
            self._setFrogPosition(x,y,view,input)
        elif input.is_key_down('right'):
            x=x-GRID_SIZE
            self._setFrogPosition(x,y,view,input)
        elif input.is_key_down('up'):
            y=y-GRID_SIZE
            self._setFrogPosition(x,y,view,input)
        elif input.is_key_down('down'):
            y=y+GRID_SIZE
            self._setFrogPosition(x,y,view,input)

    def _setFrogPosition(self, x,y ,view, input):
        """
        Sets the frog position to the desired x and y position.

        This method takes the inputs x and y and sets them as the frog's new
        position on the view window.

        Parameter input: The user input, used to control the frog and change
        state
        Precondition: input is an instance of GInput

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView and is inherited from GameApp

        Parameter x: the frog center x value to set to.
        Precondition: x is an int or a float

        Parameter y: the frog center y value to set to.
        Precondition: y is an int or a float
        """
        self.setFrogX(x)
        self.setFrogY(y)
