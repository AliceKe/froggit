"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Each lane is like its own level. It has hazards (e.g. cars) that the frog has to make
it past.  Therefore, it is a lot easier to program frogger by breaking each level into
a bunch of lane objects (and this is exactly how the level files are organized).

You should think of each lane as a secondary subcontroller.  The level is a subcontroller
to app, but then that subcontroller is broken up into several other subcontrollers, one
for each lane.  That means that lanes need to have a traditional subcontroller set-up.
They need their own initializer, update, and draw methods.

There are potentially a lot of classes here -- one for each type of lane.  But this is
another place where using subclasses is going to help us A LOT.  Most of your code will
go into the Lane class.  All of the other classes will inherit from this class, and
you will only need to add a few additional methods.

If you are working on extra credit, you might want to add additional lanes (a beach lane?
a snow lane?). Any of those classes should go in this file.  However, if you need additional
obstacles for an existing lane, those go in models.py instead.  If you are going to write
extra classes and are now sure where they would go, ask on Piazza and we will answer.

Alice Ke alk248
21.12.2020
"""
from game2d import *
from consts import *
from models import *


# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.

class Lane(object):         # You are permitted to change the parent class if you wish
    """
    Parent class for an arbitrary lane.

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """
    pass

    # LIST ALL HIDDEN ATTRIBUTES HERE
    #Attribute _objs: The list of obstacles
    # Invariant: _objs is an empty list if lane is of type grass, else it is
    #a non-empty list of obstacles for the lane

    # Attribute _speed: The lane speed
    # Invariant: _speed is an int

    # Attribute _tiles: The list containing all the tiles for the lane.
    # Invariant: _tiles is a list containing GTile objects.

    # Attribute _safeFrogs: The list that collects how many safe frogs are
    #placed on a lilypad
    # Invariant: _safeFrogs is an empty list or a list containing GImages

    # Attribute _lanes_list: The lanes list taken out from the full json loaded
    #for the level
    # Invariant: _lanes_list is a nested list with dictionaries inside.

    # Attribute _exitsOnly: The list of exits (lilypads) for the level. This
    #stores the objects type and position from the json.
    # Invariant: _exitsOnly is a list containing dictionaries that contain
    #strings.

    # Attribute _width: The width of the lane.
    # Invariant: width is an int

    # Attribute _image: The obstacle that is placed on a lane
    # Invariant: _image is an instance of GImage

    # Attribute _tile: The tile for the lane.
    # Invariant: _tile is an instance of GTile

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getObstacle(self):
        """
        Returns the obstacle (car, log, lilypad etc.)
        """
        return self._image

    def getexitsOnly(self):
        """
        Returns the list of all exits (lilypads) for the level.
        """
        return self._exitsOnly

    # INITIALIZER TO SET LANE POSITION, BACKGROUND,AND OBJECTS
    def __init__(self, json_dict, lane, hitboxjson):
        """
        Initializes the lane position, background and objects (e.g obstacles).

        Parameter json_dict: json_dict is the loaded json file for the level.
        Precondition: json_dict is a nested dictionary that is taken from the
        json loaded for the level.

        Parameter lane: lane is the position of the lane.
        Precondition: lane is an int.

        Parameter hitboxjson: hitboxjson is the loaded json file for the
        images and sprites which contain hitbox values.
        Precondition: hitboxjson is a loaded json file.
        """
        lanes_list = json_dict['lanes']
        self._initEmpty(json_dict)
        self._setTile(lanes_list, lane)
        self._tiles.append(self._tile)
        if not lanes_list[lane]['type'] == 'grass':
            objs_list = lanes_list[lane]['objects']
            for o in range(len(objs_list)):
                self._setImage(lanes_list, objs_list, o, lane)
                self._objs.append(self._image)
                if lanes_list[lane]['type'] == 'water' or \
                lanes_list[lane]['type'] == 'road':
                    self._speed = lanes_list[lane]['speed']
                else:
                    self._speed=0
                if self._speed<0:
                    self.getObstacle().angle = 180
        self._initExitsOnly(lanes_list)
        self._initHitboxImage(hitboxjson)

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def update(self, dt, json):
        """
        Controls the flow of obstacles (cars, logs and trailers).

        The movement of cars is controlled by this update method. It will enable
        cars and logs to move around 'continuously' with a wraparound
        implemented. The obstacles in each lane will move depending on the speed
        set for the lane.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter json: The full loaded json for the level.
        Precondition: json is a nested dictionary for the level.
        """
        buffer = json['offscreen']
        buffer_width = self._width + buffer * GRID_SIZE

        pixel_size = self._speed * dt

        for obstacle in self._objs:
            if self._speed !=0:
                obstacle.x = (obstacle.x+pixel_size)
            if obstacle.x>buffer_width:
                d = obstacle.x - buffer_width
                obstacle.x = -buffer * GRID_SIZE + d
            if obstacle.x<(-buffer*GRID_SIZE):
                d = -buffer*GRID_SIZE - obstacle.x
                obstacle.x = buffer_width - d

    def draw(self, view):
        """
        Draws the lane and whatever goes on the lane (i.e obstacles)

        Draws the lane tiles and the obstacles that are in each lane to the view
        window. When a safe frog is created and added to the list self._safeFrogs,
        the blue frogs will also be drawn if there are any.

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView and is inherited from GameApp
        """
        for tile in self._tiles:
            tile.draw(view)
        for obj in self._objs:
            obj.draw(view)
        for safe in self._safeFrogs:
            safe.draw(view)

    def collides(self, frog):
        """
        Returns True if the object and the frog collide. False otherwise.

        Checks if the object and the frog are colliding. The object is the lane
        or the obstacle (i.e car). This collision method takes hitboxes into
        account.

        Parameter frog: frog is the frog object
        Precondition: frog is an instance of the Frog class
        """
        if not frog is None:
            return self._tile.collides(frog)

    def contains(self, frog):
        """
        Returns True if the object contains the frog's center.

        Checks if the frog's center is within the obstacle. By default,
        this method just checks the bounding box of the shape.

        Parameter frog: frog is the frog instance
        Precondition: frog is an instance of the Frog class
        """
        return self._tile.contains((frog.x, frog.y))

    def _setTile(self, lanes_list, lane):
        """
        Creates a lane Gtile for the intiializer.

        This method will create a GTile object when called. The tile will be
        a part of creating the whole horizontal lane.

        Parameter lanes_list: The lane list from the full json loaded for the
        level.
        Precondition: lanes_list is a nested list with dictionaries inside.

        Parameter lane: The lane position from the bottom lane.
        Precondition: lane is an int
        """
        self._tile = GTile(left = 0, bottom = 0, width=self._width,height=\
        GRID_SIZE, source = lanes_list[lane]['type'] + '.png')
        self._tile.bottom += GRID_SIZE * lane

    def _setImage(self, lanes_list, objs_list, o, lane):
        """
        Initializes the lane GImage obstacles (cars etc.).

        Parameter lanes_list: The lane list from the full json loaded for the
        level.
        Precondition: lanes_list is a nested list with dictionaries inside.

        Parameter objs_list: The list of objects takeen from the json that is
        loaded for the level.
        Precondition: objs_list is a nested list with dictionaries inside.

        Parameter o: The position of the obstacle in the objects list(objs_list).
        Precondition: o is an int.

        Parameter lane: lane is the position of the lane.
        Precondition: lane is an int.
        """
        image_source = lanes_list[lane]['objects'][o]['type']
        self._image = GImage(source = image_source+'.png')
        self._image.y = self._tile.bottom+GRID_SIZE/2
        self._image.x = objs_list[o]['position']*GRID_SIZE + GRID_SIZE/2

    def _initExitsOnly(self, lanes_list):
        """
        Initializes the a list of all lilypads (exits only).

        Parameter lanes_list: The lane list from the full json loaded for the
        level.
        Precondition: lanes_list is a nested list with dictionaries inside.
        """
        for l in lanes_list:
            if l['type'] == 'hedge':
                for obstacle in l['objects']:
                    obstacletype = obstacle['type']
                    if obstacletype == 'exit':
                        self._exitsOnly.append(obstacle)

    def _initHitboxImage(self, hitboxjson):
        """
        Initializes assignment of hitbox values to all the obstacles
        e.g cars, logs etc.

        Parameter hitboxjson: hitboxjson is the loaded json file for the
        images and sprites which contain hitbox values.
        Precondition: hitboxjson is a loaded json file from 'objects.json'.
        """
        images_hitboxDict = hitboxjson['images']
        for val in images_hitboxDict:
            for obstacle in self._objs:
                    if obstacle.source == val + '.png':
                        obstacle.hitbox = images_hitboxDict[val]['hitbox']

    def _initEmpty(self, json_dict):
        """
        Initializes all the empty attributes at the start of the game.

        Helper to the initializer.

        Parameter json_dict: json_dict is the loaded json file for the level.
        Precondition: json_dict is a nested dictionary that is taken from the
        json loaded for the level.
        """
        self._objs = []
        self._tiles = []
        lanes_list = json_dict['lanes']
        self._lanes_list = lanes_list
        objs_list = []
        width = json_dict['size'][0]*GRID_SIZE
        self._width = width
        self._safeFrogs = []
        self._exitsOnly = []
        self._distance = 0


class Grass(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a 'safe' grass area.

    You will NOT need to actually do anything in this class.  You will only do anything
    with this class if you are adding additional features like a snake in the grass
    (which the original Frogger does on higher difficulties).
    """
    pass

    # ONLY ADD CODE IF YOU ARE WORKING ON EXTRA CREDIT EXTENSIONS.


class Road(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a roadway with cars.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, roads are different
    than other lanes as they have cars that can kill the frog. Therefore, this class
    does need a method to tell whether or not the frog is safe.
    """
    pass

    # DEFINE ANY NEW METHODS HERE
    def checkCarCollision(self, frog):
        """
        Checks if center of the frog is within the obstacle (e.g truck).
        Returns True if so, False otherwise.

        Parameter frog: frog is the frog instance
        Precondition: frog is an instance of the Frog class
        """
        FrogCollision = False
        for obstacle in self._objs:
                if not (frog is None) and obstacle.contains((frog.x, frog.y)):
                    FrogCollision = True
                    frog.setAnimator(None)
        return FrogCollision


class Water(Lane):
    """
    A class representing a waterway with logs.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, water is very different
    because it is quite hazardous. The frog will die in water unless the (x,y) position
    of the frog (its center) is contained inside of a log. Therefore, this class needs a
    method to tell whether or not the frog is safe.

    In addition, the logs move the frog. If the frog is currently in this lane, then the
    frog moves at the same rate as all of the logs.
    """
    pass

    # DEFINE ANY NEW METHODS HERE
    def moveFrogwithLog(self, frog, lane, dt):
        """
        Move frog by the same distance as the log it is on.

        This method will move the frog if it is sitting on a log.

        Parameter frog: frog is the frog object
        Precondition: frog is an instance of the Frog class

        Parameter lane: The lane object that the frog is on.
        Precondition: lane is of the class Water

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        for obstacle in self._objs:
            if obstacle.contains((frog.x, frog.y)):
                frog.x += lane._speed * dt

    def checkWaterCollision(self, frog):
        """
        Returns True if the frog and water are touching. False otherwise.

        This method checks if the frog is in water or on a log.

        Parameter frog: frog is the frog object
        Precondition: frog is an instance of the Frog class
        """
        FrogCollision = True
        for obstacle in self._objs:
                if  not (frog is None) and obstacle.contains((frog.x, frog.y)):
                    FrogCollision = False
        return FrogCollision


class Hedge(Lane):
    """
    A class representing the exit hedge.

    This class is a subclass of lane because it does want to use a lot of the features
    of that class. But there is a lot more going on with this class, and so it needs
    several more methods.  First of all, hedges are the win condition. They contain exit
    objects (which the frog is trying to reach). When a frog reaches the exit, it needs
    to be replaced by the blue frog image and that exit is now "taken", never to be used
    again.

    That means this class needs methods to determine whether or not an exit is taken.
    It also need to take the (x,y) position of the frog and use that to determine which
    exit (if any) the frog has reached. Finally, it needs a method to determine if there
    are any available exits at all; once they are taken the game is over.

    These exit methods will require several additional attributes. That means this class
    (unlike Road and Water) will need an initializer. Remember to user super() to combine
    it with the initializer for the Lane.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO SET ADDITIONAL EXIT INFORMATION
    def __init__(self, json_dict, lane, hitboxjson):
        """
        Intializer for the Hedge subclass.

        This method initializes the Hedge subclass.

        Parameter json_dict: json_dict is the loaded json file for the level.
        Precondition: json_dict is a nested dictionary that is taken from the
        json loaded for the level.

        Parameter lane: lane is the position of the lane.
        Precondition: lane is an int.

        Parameter hitboxjson: hitboxjson is the loaded json file for the
        images and sprites which contain hitbox values.
        Precondition: hitboxjson is a loaded json file.
        """
        super().__init__(json_dict, lane, hitboxjson)

    # ANY ADDITIONAL METHODS
    def checkHedgeExit(self, frog):
        """
        Returns True if the frog is on a valid exit or opening on the hedge,
        False otherwise.

        Checks if the hedge grid that the frog is moving to is a valid entry
        point. Valid entry includes lilypads or logs.

        Parameter frog: frog is the frog object
        Precondition: frog is an instance of the Frog class
        """
        FrogEnter = False
        for obstacle in self._objs:
            if obstacle.source == 'exit.png':
                if obstacle.collides(frog) and \
                frog.angle != FROG_SOUTH:
                    FrogEnter= True
            if obstacle.source == 'open.png':
                if obstacle.collides(frog):
                    FrogEnter= True
        return FrogEnter

    def checkHedgeOpening(self, frog):
        """
        Returns True if the frog is on an opening. False otherwise.

        Parameter frog: frog is the frog object
        Precondition: frog is an instance of the Frog class
        """
        FrogEnter = False
        for obstacle in self._objs:
            if obstacle.source == 'open.png':
                if obstacle.collides(frog):
                    FrogEnter= True
        return FrogEnter

    def SafeHedgeExit(self, frog):
        """
        Returns True if it is a valid exit (lilypad) and places a safe blue
        frog if so. False otherwise.

        Parameter frog: frog is the frog object
        Precondition: frog is an instance of the Frog class
        """
        FrogEnter = False
        for obstacle in self._objs:
            if obstacle.contains((frog.x, frog.y)) and not obstacle.source == \
            'open.png' :
                FrogEnter= True
                self._safeFrogs.append(GImage(source= FROG_SAFE, angle = \
                FROG_SOUTH, x = obstacle.x, y = obstacle.y))
        if FrogEnter:
            frog.getJumpSound().volume = 0.0
        return FrogEnter

    def blockExit(self, frog):
        """
        Allows frog to enter if exit is unoccupied by a safe frog. Else, it
        blocks movement onto the exit.

        Detects if the exit should be blocked. The exit should be blocked
        if a safe frog is on the lily pad.

        Parameter frog: frog is the frog object
        Precondition: frog is an instance of the Frog class
        """
        FrogBlock = False
        if not self._safeFrogs == []:
            for taken in self._safeFrogs:
                if frog.contains((taken.x,taken.y)):
                    FrogBlock = True
        return FrogBlock

# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
