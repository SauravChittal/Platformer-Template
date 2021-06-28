""" 
This is basically a template for creating a platformer.

It has a scrolling background made of two pictures and 2 enemies along with a playable
character and also a flag indicating a win.

There are quite a lot of things which could be done to generlize these things for multiple things
such as more backgrounds(fairly easy) to more and specialized enemies(more difficult)
"""
import random
from pygame_functions import *

# Sets the screen size and background images. These are of-course placeholders
screenSize(1000, 750)
setBackgroundImage(["background-end.jpg", "images/background-start.jpeg"])

# Creates the necessary sprites. Again placeholder image locations
main = makeSprite("[Main Char Placeholder]")
ene = makeSprite("[Enemy Placeholder2]")
ene2 = makeSprite("[Enemy Placeholder2]")
flag = makeSprite("[Flag Place]")

# These make sure that the sprite aligns with the background. Change these if different pictures are used
transformSprite(ene, 0, 0.1)
transformSprite(ene2, 0, 0.1)
transformSprite(main, 0, 0.1, hflip=True)
transformSprite(flag, 0, 0.45)
# Location stuff
# Code:
# pos = position
# g = ene
# g2 = ene2
# f = flag
# Add and change as per convinience. A list could be used to reference multiple enemies if need be
xpos = 0
ypos = 545
xspeed = 0
yspeed = 0

gxpos = 500
gypos = 595

g2xpos = 700
g2ypos = 595

fxpos = 2250

# These two boolean values are used to simulate jumping. Don't change unless you want to alter jumping mechanics
is_in_air = False
max_height_reached = False

# Used to see if the enemies should be onscreen or not. List can be extended to incorporate more enemies
onscreen = [True, True]

# True for right and False for left. Determines direction enemies have to move
gdirection = [True, True]

# Used to confirm killing of enemies
gkill = [False, False]

# Labels

time = 4800

# Shows time in top-left corner.
timelabel = makeLabel(str(80), 75, 800, 50, background="white")
showLabel(timelabel)

# Label to be shown on endscreen
endlabel = makeLabel("You have lost. Press Esc to leave", 40, 250, 188)

# Finally we move the sprites to correct locations and show them onscreen
moveSprite(main, xpos, ypos)
moveSprite(ene, gxpos, gypos)
moveSprite(ene2, g2xpos, g2ypos)
# No Special values since flag won't change pos
moveSprite(flag, 200, 105)
showSprite(main)
showSprite(ene)
showSprite(ene2)
showSprite(flag)


def crash():
    '''This function checks if main character has crashed into an enemy. Use a for loop in case of multiple enemies
     I don't need parameters to crash since I automatically update positions instantly. Can be changed for specialized enemies'''
    global xpos, gxpos, ypos, gypos, g2xpos, g2ypos, onscreen, gkill
    if (xpos <= gxpos + 5 and xpos >= gxpos - 5 and ypos >= 545) or (xpos <= g2xpos + 5 and xpos >= g2xpos - 5 and ypos >= 545):
        return True
    if xpos <= gxpos + 5 and xpos >= gxpos - 5 and ypos < 545:
        onscreen = [False, True]
        gkill = [True, False]
    if xpos <= g2xpos + 5 and xpos >= g2xpos - 5 and ypos < 545:
        onscreen[1] = False
        gkill[1] = True
    return False

while True:
    # This if-elif conditionals check the button currently being pressed. Ideally doesn't need much changing.
    if keyPressed("right") and keyPressed("y"):
        transformSprite(main, 0, 0.1)
        xpos += 10
        fxpos -= 10
        moveSprite(flag, fxpos, 105)
        scrollBackground(-10, 0)
    elif keyPressed("left") and keyPressed("y") and not is_in_air:
        transformSprite(main, 0, 0.1, hflip=True)
        xpos -= 10
        fxpos += 10
        moveSprite(flag, fxpos, 105)
        scrollBackground(10, 0)
    elif keyPressed("right"):
        transformSprite(main, 0, 0.1)
        xpos += 5
        fxpos -= 5
        moveSprite(flag, fxpos, 105)
        scrollBackground(-5, 0)
    elif keyPressed("left") and not is_in_air:
        transformSprite(main, 0, 0.1, hflip=True)
        xpos -= 5
        fxpos += 5
        moveSprite(flag, fxpos, 105)
        scrollBackground(5, 0)

    if keyPressed("b") or keyPressed("a"):
        is_in_air = True

    # This if block is for simulation of jumping. Again, ideally doesn't need change.
    # Point to note, main character gets a jump boost if he/she hits the enemy on the head
    # (When the ypos of main is more than the ypos of enemies)
    if is_in_air and max_height_reached == False:
        # Negative is going up
        ypos -= 8
        # Putting max height as 481 if he hasn't already jumped on an enemy
        # hence Mario starts to fall down after that
        max_height = 481 if gkill[0] == False and gkill[1] == False else 401
        if ypos == max_height:
            max_height_reached = True
            if gkill[0]: gkill[0] = False
            if gkill[1]: gkill[1] = False
    elif is_in_air and max_height_reached:
        # Positive ypos is going down
        ypos += 8
        # Changing the boolean values so neither conditions are fulfilled unless
        # b is pressed again
        if ypos == 545:
            is_in_air = False
            max_height_reached = False

    # Simulates movement of enemies. Again, use for loops for multiple enemies
    g1_rand = random.randint(1, 5)
    g2_rand = random.randint(3, 8)
    gxpos += g1_rand if gdirection[0] else -g1_rand
    g2xpos += g2_rand if gdirection[1] else -g2_rand

    # This ensures that the enemies never go offscreen. They bounce back if the go too far
    # If you make them go offscreen, make sure to hidesprites and change their xpos, otherwise
    # They enemies or their hitbox (which is a set of coordinates) may roll over during scrolling
    if gxpos > 960:
        gdirection[0] = False
    elif gxpos < 100:
        gdirection[0] = True
    if g2xpos > 960:
        gdirection[1] = False
    elif g2xpos < 100:
        gdirection[1] = False

    # Makes sure the main character is on screen always
    if xpos > 960:
        xpos = -100
    elif xpos < -100:
        xpos = 960

    # Game should end when you crash into an enemy
    if crash():
        showLabel(endlabel)
        endWait()

    # Finally, after changing their positions, make sure that they are in the appropriate place
    # It seems annoying for multiple enemies.
    moveSprite(main, xpos, ypos)
    if onscreen[0] and onscreen[1]:
        moveSprite(ene, gxpos, gypos)
        moveSprite(ene2, g2xpos, g2ypos)
    elif onscreen[0] == False:
        moveSprite(ene2, g2xpos, g2ypos)
        hideSprite(ene)
        gxpos = gypos = 1000
    elif onscreen[1] == False:
        moveSprite(ene, gxpos, gypos)
        hideSprite(ene2)
        g2ypos = g2ypos = 1000

    # If you've killed an enemy, this ensures you get the boost
    if gkill[0] or gkill[1]:
        is_in_air = True

    # You win when you touch the flag
    if touching(flag, main):
        changeLabel(endlabel, "You've won yaay", fontColour="Blue")
        hideAll()
        showLabel(endlabel)
        endWait()

    # Shows the time. Do change it to make it look better
    time -= 1
    if time == 0:
        showLabel(endlabel)
        endWait()
    if time % 60 == 0:
        changeLabel(timelabel, str(int(time) / 60), background='white')

    tick(30)

endWait()