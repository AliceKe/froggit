"""
Models module for Froggit

This module contains the model classes for the Frogger game. Anything that you
interact with on the screen is model: the frog, the cars, the logs, and so on.

Just because something is a model does not mean there has to be a special class for
it. Unless you need something special for your extra gameplay features, cars and logs
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object.

That is why this module contains the Frog class.  There is A LOT going on with the
frog, particularly once you start creating the animation coroutines.

If you are just working on the main assignment, you should not need any other classes
in this module. However, you might find yourself adding extra classes to add new
features.  For example, turtles that can submerge underneath the frog would probably
need a custom model for the same reason that the frog does.

If you are unsure about  whether to make a new class or not, please ask on Piazza. We
will answer.

Alice Ke alk248
21.12.2020
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from a lane or level object, then it
# should be a parameter in your method.


class Frog(GSprite):         # You will need to change this by Task 3
    """
    A class representing the frog

    The frog is represented as an image (or sprite if you are doing timed animation).
    However, unlike the obstacles, we cannot use a simple GImage class for the frog.
    The frog has to have additional attributes (which you will add).  That is why we
    make it a subclass of GImage.

    When you reach Task 3, you will discover that Frog needs to be a composite object,
    tracking both the frog animation and the death animation.  That will like caused
    major modifications to this class.
    """
    pass
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _animator: A coroutine for performing the frog animation
    # Invariant: _animator is a generator-based coroutine (or None)

    # Attribute _speed: The speed of the frog instance
    # Invariant: _speed is an int or float

    # Attribute _jumpSound: The sound to play when the frog jumps
    # Invariant: _jumpSound is a Sound object

    # Attribute _deathSound: The sound to play when the frog dies
    # Invariant: _deathSound is a Sound object

    # Attribute _exitSound: The sound to play when the frog reaches an exit
    # Invariant: _exitSound is a Sound object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAnimator(self):
        """
        Returns frog animator when called.

        This is a getter which will return the value of the self._animator.
        """
        return self._animator

    def setAnimator(self, val):
        """
        Method to set the frog animator to the given value val.

        Parameter val: the value to set the animator to.
        Precondition: val is a method or None
        """
        self._animator = val

    def getJumpSound(self):
        """
        Returns the value of the attribute self._jumpSound
        """
        return self._jumpSound

    # INITIALIZER TO SET FROG POSITION
    def __init__(self, x, y, format, source, hitboxes, hitboxjson):
        """
        Initializes the frog and all its attributes.

        The initializer will create the frog and the other attributes at the
        start of the game.

        Parameter x: the x value for the frog's intial position
        Precondition: x is an int or a float

        Parameter y: the y value for the frog's intial position
        Precondition: y is an int or a float

        Parameter format: The frog sprite format taken from the 'objects.json'
        json file under the 'format'
        Precondition: format is a list of ints and has a length of 2.

        Parameter source: The sprite source taken from the 'objects.json'
        json file under the 'file'
        Precondition: source is a string

        Parameter hitboxes: The hitboxes for the frog sprite.
        Precondition: hitboxes is a tuple with the frog hitboxe values

        Parameter hitboxjson: hitboxjson is the loaded 'objects.json' json file
        for the images and sprites which contain hitbox values.
        Precondition: hitboxjson is a loaded json file.
        """
        super().__init__(x= x*GRID_SIZE + GRID_SIZE/2, y = y*GRID_SIZE + \
        GRID_SIZE/2,source= source, format = format, hitboxes = hitboxes)
        self.angle = FROG_NORTH
        self.frame = 0
        self._animator = None
        self._speed = FROG_SPEED
        self._jumpSound = Sound(CROAK_SOUND)
        self._deathSound = Sound(SPLAT_SOUND)
        self._exitSound = Sound(TRILL_SOUND)

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def update(self, input, dt, view):
        """
        Animates the frog.

        This method uses the user input to control whether the frog should be
        animated.

        Parameter input: The player input.
        Precondition: input is an instance of GInput

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView and is inherited from GameApp
        """
        if not self._animator is None:          # We have something to animate
            try:
                self._animator.send(dt)         # Tell it how far to animate
            except:
                self._animator = None        # Stop animating
        elif input.is_key_down('left'):
            self._animator = self._animate_slide('left')
            next(self._animator) # Start up the animator
            self._readyToMove = False
        elif input.is_key_down('right'):
            self._animator = self._animate_slide('right')
            next(self._animator) # Start up the animator
            self._readyToMove = False
        elif input.is_key_down('up'):
            self._animator = self._animate_slide('up')
            next(self._animator) # Start up the animator
            self._readyToMove = False
        elif input.is_key_down('down'):
            self._animator = self._animate_slide('down')
            next(self._animator) # Start up the animator
            self._readyToMove = False

    def playExitSound(self):
        """
        Plays the exit sound when called.
        """
        self._exitSound.play()

    def playDeathSound(self):
        """
        Plays the death sound when called.
        """
        self._deathSound.play()

    def _animate_slide(self, direction):
        """
        Animates the sliding movement of the frog over FROG_SPEED seconds

        This method is a coroutine that takes a break every time it moves the
        frog. The coroutine takes the dt as periodic input so it knows how
        many (parts of) seconds to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: The direction to slide.
        Precondition: direction is a string and one of 'up','down', 'left' or
        'right.'
        """
        s_vert = self.y
        s_hor = self.x
        #Set final values (vertical and horizontal) to the initial values since
        #movement is always in one direction (i.e only x or only y changes)
        f_vert = s_vert
        f_hor = s_hor
        if direction == 'down':
            f_vert = self.y - GRID_SIZE
        elif direction == 'up':
            f_vert = self.y + GRID_SIZE
        elif direction == 'left':
            f_hor = self.x - GRID_SIZE
        else:
            f_hor = self.x + GRID_SIZE

        amt = GRID_SIZE/FROG_SPEED
        animating = True
        while animating:
            dt = (yield)
            distance = amt*dt
            self._animateDown(s_vert, f_vert, distance, direction)
            self._animateUp(s_vert, f_vert, distance, direction)
            self._animateLeft(s_hor, f_hor, distance, direction)
            self._animateRight(s_hor, f_hor, distance, direction)

            if abs(self.y - s_vert) >= GRID_SIZE or abs(self.x - s_hor) >= \
            GRID_SIZE:
                animating = False
                self.y = round((f_vert-GRID_SIZE/2)/GRID_SIZE)*GRID_SIZE + \
                GRID_SIZE/2
                self.x = f_hor
                self._animator = None

    def _animateDown(self,s_vert, f_vert, distance, direction):
        """
        Calculates all the values needed to animate the frog in a downwards
        direction.

        This method will animate the frog in the downwards direction.

        Parameter s_vert: The start frog position in the vertical direction
        Precondition: s_vert is a int or float

        Parameter f_vert: The final frog position in the vertical direction
        Precondition: f_vert is a int or float

        Parameter distance: The distance to slide the frog by.
        Precondition: distance is an int or float

        Parameter direction: The direction to slide.
        Precondition: direction is a string and one of 'up','down', 'left' or
        'right.'
        """
        if direction == 'down':
            self._jumpSound.play()
            self.y -=distance
            frac = 2*(self.y-s_vert)/(f_vert-s_vert)
            if frac<1:
                frame = FROG_START+frac*(FROG_MIDPT-FROG_START)
                self.frame = round(frame)
            else:
                frame = FROG_END - FROG_MIDPT*frac
                self.frame = round(frame)

    def _animateUp(self,s_vert, f_vert, distance, direction):
        """
        Calculates all the values needed to animate the frog in an upwards
        direction.

        Parameter s_vert: The start frog position in the vertical direction
        Precondition: s_vert is a int or float

        Parameter f_vert: The final frog position in the vertical direction
        Precondition: f_vert is a int or float

        Parameter distance: The distance to slide the frog by.
        Precondition: distance is an int or float

        Parameter direction: The direction to slide.
        Precondition: direction is a string and one of 'up','down', 'left' or
        'right.'
        """
        if direction == 'up':
            self._jumpSound.play()
            self.y += distance
            frac = 2*(self.y-s_vert)/(f_vert-s_vert)
            if frac<1:
                frame = FROG_START+frac*(FROG_MIDPT-FROG_START)
                self.frame = round(frame)
            else:
                frame = FROG_END - FROG_MIDPT *frac
                self.frame = round(frame)

    def _animateLeft(self, s_hor, f_hor, distance, direction):

        """
        Calculates the amount to slide for left direction.

        This is a helper to the _animate_slide method.

        Parameter s_hor: The start frog position in the horizontal direction
        Precondition: s_hor is a int or float

        Parameter f_hor: The final frog position in the horizontal direction
        Precondition: f_hor is a int or float

        Parameter distance: The distance to slide the frog by.
        Precondition: distance is an int or float

        Parameter direction: The direction to slide.
        Precondition: direction is a string and one of 'up','down', 'left' or
        'right.'
        """
        if direction == 'left':
            self._jumpSound.play()
            self.x -= distance
            frac = 2*(self.x-s_hor)/(f_hor-s_hor)
            if frac<1:
                frame = FROG_START+frac*(FROG_MIDPT-FROG_START)
                self.frame = round(frame)
            else:
                frame = FROG_END - FROG_MIDPT *frac
                self.frame = round(frame)

    def _animateRight(self, s_hor, f_hor, distance, direction):
        """
        Calculates the amount to slide for the right direction.

        Parameter s_hor: The start frog position in the horizontal direction
        Precondition: s_hor is a int or float

        Parameter f_hor: The final frog position in the horizontal direction
        Precondition: f_hor is a int or float

        Parameter distance: The distance to slide the frog by.
        Precondition: distance is an int or float

        Parameter direction: The direction to slide.
        Precondition: direction is a string and one of 'up','down', 'left' or
        'right.'
        """
        if direction == 'right':
            self._jumpSound.play()
            self.x += distance
            frac = 2*(self.x-s_hor)/(f_hor-s_hor)
            if frac<1:
                frame = FROG_START+frac*(FROG_MIDPT-FROG_START)
                self.frame = round(frame)
            else:
                frame = FROG_END - FROG_MIDPT *frac
                self.frame = round(frame)

# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
