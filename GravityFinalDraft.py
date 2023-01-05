# Byron Xu (bx7ugx)
"""
Two player game, player 1 and player 2 are ALWAYS opposite gravities from one another.

Power-ups included, such as increasing speed, reversing direction, flipping gravity, etc.
Works similarly to a platforming game except the camera doesn't scroll (might change later).

Falling out of the map or running into spikes results in a GAME OVER.

Static camera (no time), 800 x 600 screen dimensions.

All levels are possible in multiple ways, including without ever using the gravity flip.
Most levels are puzzles that involve using gravity flipping though.

OPTIONAL REQS:
    - Collectibles (Power-ups and coins)
    - Two players simultaneously
    - Graphics/Images
    - Sprite Animation
    - Restart from Game Over
    - Health Bar

ADDITIONAL FEATURES:
    - Button animations for hovering mouse over
    - Intro screen and clickable buttons
    - Double jumping as power-up
    - Idle animation
    - Directional animation
    - Shop, RPG-like text
    - Pause screen/Help screen

NOTE: Moved sprites outside of camera as "deletion" rather than putting them as a list
and list.removing them as a failsafe against crashing (as list.remove()) crashes if the
object is nonexistent). Would eventually cause lag if game had more levels.

Code is a bit messy and some lines could be rewritten as functions but it's gotten kinda
big and no time soooo...

TO-DO LIST:
    - Add more levels
    - Add boss fight
    - Add "mouse hovering over button" function for simplification
    - Add exit button to game over screen
    - Add Achievements (progress saveable)
    - Change numbers to variables that they're related to (e.g. y = 300 to CAMERAHEIGHT // 2)

BUGS:
    - For some reason, if I end a level with an if function for the gate/pressure plate
    mechanic, the game becomes extremely fast. It's not a tick issue as I changed that,
    so I'm thinking it may be related to the gamebox programming as I don't know exactly
    how it's programmed.

    5/5/21 3:13PM

5/6/21 5:17PM
    - sorry for the messy code in levels 7+, those were stuff i did today and
    yesterday and didn't have the brainpower to organize it into functions
"""
import pygame
import gamebox
import random

CAMERAWIDTH, CAMERAHEIGHT = 800, 600
camera = gamebox.Camera(CAMERAWIDTH, CAMERAHEIGHT)

RESPAWNCOORDS = [70, 450]
wallcolor = "black"
SPEED = 8
DEFAULTSPEED = 8
GRAVITY = 2
gravityCooldown = 0
textCounter = 0
showText = []
COINS = 0
LEVEL = 1
LIVES = 3
P2ALIVE = 1
DO_ONCE = 1
GODMODE = 0
JUMPHEIGHT = 25
INTROSCREEN = "Intro"
PAUSE = 0
YSPEEDLIMIT = 10
SLOWFALL = 0
NPC1GIFT = 0
SAVELEVEL = 1
KEYGET = 0
movingPlatformCounter = 0
platformXChange = 5

# achievements: (potentially dropped due to lack of time)
gravityCounter = 0

# SPRITES:
game_over_screen = gamebox.from_image(CAMERAWIDTH // 2, CAMERAHEIGHT // 2 - 100, "game_over_screen_transparent.png")
game_over_screen.scale_by(.75)

frame = 0

door_sheet = gamebox.load_sprite_sheet("door_sprite_sheet.png", 4, 3)
door = gamebox.from_image(200, 240, door_sheet[frame])
# HEART/LIVES SPRITES
life1 = gamebox.from_image(50, 50, "transparent_heart_sprite.png") # separate for
life2 = gamebox.from_image(50, 75, "transparent_heart_sprite.png") # easier removal
life3 = gamebox.from_image(50, 100, "transparent_heart_sprite.png") # instead of copying
life4 = gamebox.from_image(50, 125, "transparent_heart_sprite.png")
life1.scale_by(.1), life2.scale_by(.1), life3.scale_by(.1), life4.scale_by(.1)

spikes = gamebox.from_image(500, 45, "spikes_sprite_transparent.png")
spikes.scale_by(.15)
chocolate = gamebox.from_image(1000, 100, "chocolate_sprite.png")
chocolate.scale_by(.15)
GETGUN = 0
featherCounter = 0

npc1_sprite_sheet = gamebox.load_sprite_sheet("npc_sitting_transparent.png", 1, 3)
npc1_frame = 0
npc1 = gamebox.from_image(1000, 550, npc1_sprite_sheet[npc1_frame + 1])
npc1.scale_by(1.75)

winScreen = gamebox.from_image(400, 250, "you_win_screen_transparent.png")
caveBackground = gamebox.from_image(400, 300, "cave_background.png")
introBackground = gamebox.from_image(400, 300, "space_background_pixel_art.png")
gun = gamebox.from_image(250, 200, "gun_sprite_transparent.png")
# GRAVITY RING VARIABLES AND SPRITE
ring_sprite = gamebox.from_image(600, 550, "ring_sprite_transparent.png")
ring_sprite.scale_by(.1)
ringGet = 1 # Set it to 1, changes to 2 because gravity cooldown is divided by this (confusing var name i know)
ringCounter = 0
# EXTRA LIFE VARIABLES AND SPRITE
extra_life = gamebox.from_image(300, 550, "transparent_heart_sprite.png")
extra_life.scale_by(.1)
extraLifeGet = 0
extraLifeCounter = 0

# DOUBLE JUMP VARIABLES AND SPRITE
double_jump = gamebox.from_image(450, 550, "double_jump_sprite_transparent.png")
double_jump.scale_by(.17)
doubleJumpCounter = 0
doubleJumpGet = 0
canJump = 1
jumpCooldown = 30
# PLAYER 2 INITIAL SPRITE SETUP
doggo_sheet = gamebox.load_sprite_sheet("dog_sprite_sheet_walking_transparent.png", 1, 8)
doggo_frame = 0
doggo_counter = 0
doggo_direction = "right"
doggo_idle_sheet = gamebox.load_sprite_sheet("dog_idle.png", 1, 3)
doggo_idle_frame = 0
doggo_idle_sheet_left = gamebox.load_sprite_sheet("dog_idle_left.png", 1, 3)
player2 = gamebox.from_image(20, 450, doggo_sheet[doggo_frame])
player2.scale_by(.75)
player2.rotate(180)
player2.flip()
idle_counter = 0
# PLAYER 1 INITIAL SPRITE SETUP
sprite_list = []
character_sheet = gamebox.load_sprite_sheet("crewmate_walk_final2_transparent.png", 1, 10)
character_frame = 5
character_counter = 0
player1 = gamebox.from_image(RESPAWNCOORDS[0], RESPAWNCOORDS[1], character_sheet[character_frame])
sprite_direction = "right"
player1.scale_by(1.5)
# FEATHER SLOW FALL SPRITE
feather_sprite = gamebox.from_image(400, 400, "feather_sprite.png")
feather_sprite.scale_by(.15)
shop_sign = gamebox.from_image(1000, 400, "shop_sign_transparent.png")
shop_sign.scale_by(.08)

key_sprite = gamebox.from_image(110, 50, "key_sprite.png")
key_sprite.scale_by(.2)
walls = []
genCoin = []

# BUTTON SPRITES:
play_sprite_sheet = gamebox.load_sprite_sheet("play_button_sprite_transparent.png", 1, 2)
playFrame = 0
help_sprite_sheet = gamebox.load_sprite_sheet("help_button_sprite_transparent.png", 1, 2)
helpFrame = 0
close_sprite_sheet = gamebox.load_sprite_sheet("close_button_sprite_transparent.png", 1, 2)
closeFrame = 0

#BOSS FIGHT:
big_red_button = gamebox.from_image(700, 200, "red_button_sprite.png")
big_red_button.scale_by(.2)
bossFlipGravity = 0
startBossAnimation = 0
bossGravityFlipSpeed = 1

magikoopa_sprite_sheet = gamebox.load_sprite_sheet("magikoopa_sprite_sheet_transparent_casting_shorter.png", 2, 10)
# THIS SPRITE SHEET WASTED 1 HOUR OF MY TIME DURING FINALS ahhHHH
magikoopaFrameCounter = 0
magikoopaFrame = 0
boss = gamebox.from_image(700, 133, magikoopa_sprite_sheet[magikoopaFrame])
boss.scale_by(1.5)
bossSpikes = gamebox.from_image(1000, 2000, "spikes_sprite_transparent.png")
bossSpikes.rotate(180)
bossSpikes.scale_by(.15)
bossLives = 3
bossSpikes2 = gamebox.from_image(1000, 2000, "spikes_sprite_transparent.png")
bossSpikes2.rotate(180)
bossSpikes2.scale_by(.15)
bossDirection = "left"
platform10Change = 5
moving10PlatformCounter = 0


def draw_help_screen():
    """
    This function draws the help screen and instructions. This can be accessed by pressing
    the question mark in game, or the "Help" button in the intro function screen.
    """
    global closeFrame
    closeButton = gamebox.from_image(50, 120, close_sprite_sheet[closeFrame])
    closeButton.scale_by(.75)

    camera.clear('black')
    introBackground = gamebox.from_image(400, 300, "space_background_pixel_art.png")
    camera.draw(introBackground)
    instruction1 = gamebox.from_text(CAMERAWIDTH // 2, 110, "Press 'G' to flip gravity!", 32, 'white')
    instruction2 = gamebox.from_text(CAMERAWIDTH // 2, 185, "Arrow keys move P1, WASD moves P2!", 32, 'white')
    instruction3 = gamebox.from_text(CAMERAWIDTH // 2, 260, "Collect coins and powerups for hidden abilities!", 32,
                                     'white')
    instruction4 = gamebox.from_text(CAMERAWIDTH // 2, 335, "Don't lose all your lives!", 32, 'white')
    instruction5 = gamebox.from_text(CAMERAWIDTH // 2, 410, "Certain colors may be correlated...", 32, 'white')
    instruction6 = gamebox.from_text(CAMERAWIDTH // 2, 485, "Only P1 can enter doors, by pressing UP!", 32, 'white')
    camera.draw(instruction1)
    camera.draw(instruction2)
    camera.draw(instruction3)
    camera.draw(instruction4)
    camera.draw(instruction5)
    camera.draw(instruction6)


def help():
    """
    This function calls the draw_help_screen() function to draw a help screen, then
    also adds the animation for hovering over a the "X" close button on the help screen,
    where clicking it changes the screen back to the intro screen.
    """
    global INTROSCREEN, closeFrame
    closeButton = gamebox.from_image(50, 120, close_sprite_sheet[closeFrame])
    closeButton.scale_by(.75)
    if INTROSCREEN == "Help":
        draw_help_screen()
        mousex, mousey = camera.mouse
        if closeButton.contains(mousex, mousey):
            closeFrame = 1
            camera.draw(closeButton)
            if camera.mouseclick:
                INTROSCREEN = "Intro"
                closeFrame = 0
        else:
            closeFrame = 0
            camera.draw(closeButton)


def intro(intro_keys):
    """
    This function is called 30 times a second and draws the intro screen of the game.
    It also contains the animations for the play button, help button, and other buttons.
    Pressing "Play" or "Gravity" will stop the loop and proceed onto the actual game
    tick() loop.
    :param intro_keys: This is a parameter for "keys" that is required to use the
    timer_loop, but is not used.
    """
    global playFrame, helpFrame, closeFrame, INTROSCREEN

    introBackground = gamebox.from_image(400, 300, "space_background_pixel_art.png")
    camera.draw(introBackground)
    introText = gamebox.from_text(400, 200, "GRAVITY", 60, 'white')
    camera.draw(introText)

    playButton = gamebox.from_image(250, 350, play_sprite_sheet[playFrame])
    helpButton = gamebox.from_image(550, 350, help_sprite_sheet[helpFrame])

    mousex, mousey = camera.mouse
    help()
    if INTROSCREEN == "Intro":
        if playButton.contains(mousex, mousey):
            playFrame = 1
            camera.draw(playButton)
            if camera.mouseclick:
                gamebox.stop_loop()
        else:
            playFrame = 0
            camera.draw(playButton)

        if helpButton.contains(mousex, mousey):
            helpFrame = 1
            camera.draw(helpButton)
            if camera.mouseclick:
                INTROSCREEN = "Help"
        else:
            helpFrame = 0
            camera.draw(helpButton)

        if introText.contains(mousex, mousey):
            introText = gamebox.from_text(400, 200, "GRAVITY", 60, 'red')
            camera.draw(introText)
            if camera.mouseclick:
                gamebox.stop_loop()

    camera.display()


gamebox.timer_loop(30, intro)


def sprite_movement(p_keys):
    """
    This function controls the sprite animation of player 1, the Among Us crewmate.
    :param p_keys: This parameter takes in "keys" pressed.
    """
    global character_frame
    global character_counter
    global sprite_direction

    character_counter += 1
    # print(sprite_direction)

    if character_counter % 8 == 0:
        character_frame += 1
        if character_frame > 8:  # only use moving sprites
            character_frame -= 1

        if sprite_direction == "left" and character_frame >= 4:
            character_frame = 0
        if sprite_direction == "right" and (character_frame >= 8 or character_frame <= 4):
            character_frame = 5

        player1.image = character_sheet[character_frame]

def doggo_sprite_movement(p_keys):
    """
    This function controls the animation of player 2, the doggo. Idle animation not included
    in this function.
    :param p_keys: This takes in the "keys" pressed.
    """
    global doggo_frame
    global doggo_counter
    global doggo_direction
    global doggo_idle_frame

    doggo_counter += 1

    if doggo_counter % 8 == 0:
        doggo_frame += 1
        if doggo_frame >= 8:
            doggo_frame = 0
        if doggo_direction == "right" and doggo_frame >= 4:
            doggo_frame = 0
        if doggo_direction == "left" and (doggo_frame >= 8 or doggo_frame <= 4):
            doggo_frame = 5
        player2.image = doggo_sheet[doggo_frame]

def doggo_idle_sprites():
    """
    This function contains the sprite animations for the idle player 2 dog,
    corresponding to the last direction the player faced.
    """
    global idle_counter, doggo_idle_frame

    idle_counter += 1

    if doggo_direction == "right":
        if idle_counter % 12 == 0:
            doggo_idle_frame += 1
            if doggo_idle_frame >= 2:
                doggo_idle_frame = 0
            player2.image = doggo_idle_sheet[doggo_idle_frame]

        if idle_counter % 180 == 0:
            doggo_idle_frame = 2
            player2.image = doggo_idle_sheet[doggo_idle_frame]

    elif doggo_direction == "left":
        if idle_counter % 12 == 0:
            doggo_idle_frame += 1
            if doggo_idle_frame >= 2:
                doggo_idle_frame = 0
            player2.image = doggo_idle_sheet_left[doggo_idle_frame]

        if idle_counter % 180 == 0:
            doggo_idle_frame = 2
            player2.image = doggo_idle_sheet_left[doggo_idle_frame]
    else:
        player2.image = doggo_idle_sheet_left[doggo_idle_frame]

def pause_game():
    """
    This function "pauses" the game by freezing the player, preventing them from moving or
    changing gravity.
    """
    global SPEED, GRAVITY, PAUSE, showText, gravityCooldown, DEFAULTSPEED

    if PAUSE == 1:
        player1.yspeed = 0
        player2.yspeed = 0
        player1.xspeed = 0
        player2.xspeed = 0
        SPEED = 0
        gravityCooldown = 20
    else:
        SPEED = DEFAULTSPEED

        if "choco" in showText:
            SPEED = 12

def achievements():
    """
    call this function only at END or at START screen. Might not have time to implement.
    :return:
    """
    global LIVES
    """
    if WIN == 1:
        if LIVES == 3:

        if gravity_counter == 0:
            achievement called "Is this easy mode?"

    """

def gravity():
    """
    This function makes players accelerate at the rate of the GRAVITY variable.
    The variable is negated when 'G' is pressed in the powerups() function, making
    gravity effectively 'flipped'.
    """
    global GRAVITY, LEVEL
    player2.yspeed += GRAVITY
    player2.y = player2.y - player2.yspeed

    player1.yspeed += GRAVITY
    player1.y = player1.y + player1.yspeed

    if LEVEL == 10:
        boss.yspeed += .5
        boss.y = boss.y + boss.yspeed

def movement(p_keys):
    """
    This function controls the movement of the players and also sets the current
    sprite direction. If no keys are pressed, the animation becomes idle (no idle
    animation for player 1, sitting animation for player 2).
    :param p_keys: Keys being pressed.
    """
    global sprite_direction, doggo_direction

    if pygame.K_LEFT in p_keys:
        sprite_direction = "left"
        player1.x -= SPEED * 1

    if pygame.K_RIGHT in p_keys:
        sprite_direction = "right"
        player1.x += SPEED * 1

    if not (pygame.K_LEFT in p_keys or pygame.K_RIGHT in p_keys):
        if sprite_direction == "right":
            player1.image = character_sheet[8] # Right player 1 idle sprite
        elif sprite_direction == "left":
            player1.image = character_sheet[9] # Left player 1 idle sprite
    else:
        sprite_movement(p_keys)

    if pygame.K_a in p_keys:  # you can check which keys are being pressed
        player2.x -= SPEED * 1
        doggo_direction = "left"

    if pygame.K_d in p_keys:  # you can check which keys are being pressed
        player2.x += SPEED * 1
        doggo_direction = "right"

    if not (pygame.K_a in p_keys or pygame.K_d in p_keys):
        doggo_idle_sprites() # Player 2 idle animation

    else:
        doggo_sprite_movement(p_keys) # Player 2 movement animation

    gravity()
    # print(player1.yspeed, player2.yspeed)

def powerups(p_keys):
    """
    This function contains all the powerups the player can attain in the game. 'G' flips
    the gravity (allowed every 20 ticks).
    :param p_keys: Keys being pressed.
    """
    global GRAVITY
    global gravityCooldown, gravityCounter
    global LEVEL
    global GODMODE, SLOWFALL, YSPEEDLIMIT
    global ringGet

    gravityCooldown -= 1 * ringGet

    if LEVEL != 'Game Over': # BUG FIX: Prevents flipping sprite in Game Over screen
        if pygame.K_g in p_keys and gravityCooldown <= 0:
            GRAVITY *= -1
            gravityCooldown = 20
            gravityCounter += 1
            player1.rotate(180)  # flips sprites alongside gravity
            player1.flip()
            player2.rotate(180)
            player2.flip()


    if SLOWFALL == 1: # Sets yspeed limit for both players, acting as a "slow fall"
        if player1.yspeed > YSPEEDLIMIT and GRAVITY > 0:
            player1.yspeed = YSPEEDLIMIT
        if player2.yspeed > YSPEEDLIMIT and GRAVITY > 0:
            player2.yspeed = YSPEEDLIMIT
        if player1.yspeed < -YSPEEDLIMIT and GRAVITY < 0:
            player1.yspeed = -YSPEEDLIMIT
        if player2.yspeed < -YSPEEDLIMIT and GRAVITY < 0:
            player2.yspeed = -YSPEEDLIMIT

    if GODMODE == 1: # Used for debugging, no gravity.
        GRAVITY = 0
        player2.yspeed = 0
        if pygame.K_UP in p_keys:
            player1.y -= SPEED * 1
        if pygame.K_DOWN in p_keys:
            player1.y += SPEED * 1
        if pygame.K_w in p_keys:
            player2.y -= SPEED * 1
        if pygame.K_s in p_keys:
            player2.y += SPEED * 1


def player_lives():
    """
    This function determines the # of player lives, and draws and removes the sprites
    accordingly. When LIVES = 0, Game Over screen is created.
    """
    global LEVEL
    if isinstance(LEVEL, int): # Removes lives in help (clicking red question mark)
        if LIVES >= 1:
            camera.draw(life1)
            if LIVES >= 2:
                camera.draw(life2)
                if LIVES >= 3:
                    camera.draw(life3)
                    if LIVES == 4:
                        camera.draw(life4)
        else:
            LEVEL = 'Game Over'


def boundary_action():
    """
    This function controls the boundary actions for the two players. Players are prevented
    from leaving the right and left sides of the camera. Falling off the screen vertically
    by 50 pixels will result in a death and teleporting the player back to spawn.
    """
    global LIVES, SPEED, P2ALIVE
    # print(bossSpikes.center, bossSpikes2.center, boss.center, spikes.center)
    if player1.y > CAMERAHEIGHT + 50 or player1.y < -50:
        LIVES -= 1
        tp_to_spawn(player1)
        tp_to_spawn(player2)

    if player1.x + 10 >= CAMERAWIDTH:
        player1.x -= SPEED * 1
    elif player1.x - 10 <= 0:
        player1.x += SPEED * 1

    if player2.x + 25 >= CAMERAWIDTH:
        player2.x -= SPEED * 1
    elif player2.x - 25 <= 0:
        player2.x += SPEED * 1

    if player2.y > CAMERAHEIGHT + 50 or player2.y < -50:
        LIVES -= 1
        tp_to_spawn(player1)
        tp_to_spawn(player2)


def create_text(p_keys):
    """
    Function creates the vast majority of the text in the game outside of the intro screen.
    List of showText checks which powerups are inside the list; if a powerup is inside the
    list (powerup collected), a text appears above the player describing the powerup for 3
    seconds. Contains shop text (when LEVEL == 6), npc text, and the help button.
    :param p_keys: Keys being pressed.
    """
    global textCounter, showText, COINS, LEVEL, GETGUN, NPC1GIFT, gravityCooldown, LIVES
    global featherCounter, SAVELEVEL, ringCounter, ringGet
    global doubleJumpCounter, doubleJumpGet, extraLifeGet, extraLifeCounter

    helpButton = gamebox.from_image(CAMERAWIDTH - 25, 55, "question_mark_sprite_transparent.png")
    helpButton.scale_by(.37)  # make transparent later
    camera.draw(helpButton)

    mousex, mousey = camera.mouse
    if LEVEL != 'Game Over' and LEVEL != 'Win': # BUG FIX: Prevents clicking hidden help sprite in game over screen
        if helpButton.contains(mousex, mousey):
            if LEVEL != 'Help':
                SAVELEVEL = LEVEL
            helpButton.scale_by(1.2)
            camera.draw(helpButton)
            if camera.mouseclick:
                LEVEL = 'Help'

    coinText = gamebox.from_text(CAMERAWIDTH - 100, CAMERAHEIGHT - 50, "Coins: " + str(COINS), 32, 'white')
    camera.draw(coinText)

    chocoText = gamebox.from_text(player1.x, player1.y - 40, "Speed Up!", 24, 'white')
    if "choco" in showText:
        textCounter += 1
        if textCounter <= 150:  # Show chocoText for 150 ticks once chocolate sprite `coll`ected
            camera.draw(chocoText)

    if player1.touches(npc1) and LEVEL == 5:
        if GETGUN == 0:
            npc1Text = gamebox.from_text(500, 525, "i lost my gun...", 18, 'white')
            npc1TextContinued = gamebox.from_text(500, 540, "can you help me find it?", 18, 'white')
            camera.draw(npc1Text)
            camera.draw(npc1TextContinued)
        if GETGUN == 1 and NPC1GIFT == 0:
            NPC1GIFT = 1
        if GETGUN == 1 and NPC1GIFT == 1:
            npc1TextAfter = gamebox.from_text(500, 525, "thank you so much,", 18, 'white')
            npc1Text2 = gamebox.from_text(500, 540, "take this!", 18, 'white')
            camera.draw(npc1TextAfter)
            camera.draw(npc1Text2)
    featherText = gamebox.from_text(player1.x, player1.y - 40, "Slow fall get!", 24, 'white')
    if "feather" in showText:
        featherCounter += 1
        if featherCounter <= 150:
            camera.draw(featherText)

    levelText = gamebox.from_text(675, 50, "Level " + str(LEVEL), 48, 'white')
    camera.draw(levelText)

    ringPrice = gamebox.from_text(ring_sprite.x, ring_sprite.y - 30, "20 Coins", 24, 'white')
    ringPowerup = gamebox.from_text(player1.x, player1.y - 40, "Gravity cooldown down!", 24, 'white')
    if player1.touches(ring_sprite) and LEVEL == 6:
        camera.draw(ringPrice)
        if COINS >= 20 and pygame.K_SPACE in p_keys:
            COINS -= 20
            ringGet = 2

    doubleJumpPrice = gamebox.from_text(double_jump.x, double_jump.y - 30, "15 Coins", 24, 'white')
    doubleJumpText = gamebox.from_text(player1.x, player1.y - 40, "Doublejump unlocked!", 24, 'white')
    if player1.touches(double_jump) and LEVEL == 6:
        camera.draw(doubleJumpPrice)
        if COINS >= 15 and pygame.K_SPACE in p_keys:
            COINS -= 15
            doubleJumpGet = 1

    extraLifePrice = gamebox.from_text(extra_life.x, extra_life.y - 30, "10 Coins", 24, 'white')
    extraLifeText = gamebox.from_text(player1.x, player1.y - 40, "Extra Life!", 24, 'white')
    if player1.touches(extra_life) and LEVEL == 6:
        camera.draw(extraLifePrice)
        if COINS >= 10 and pygame.K_SPACE in p_keys:
            COINS -= 10
            LIVES += 1
            extraLifeGet = 1

    if ringGet == 2:
        ring_sprite.center = [1000, 1000]
        ringCounter += 1
        if ringCounter <= 150:
            camera.draw(ringPowerup)

    if extraLifeGet == 1:
        extra_life.center = [1000, 1000]
        extraLifeCounter += 1
        if extraLifeCounter <= 150:
            camera.draw(extraLifeText)

    if doubleJumpGet == 1:
        double_jump.center = [1000, 1000]
        doubleJumpCounter += 1
        if doubleJumpCounter <= 150:
            camera.draw(doubleJumpText)

    if LEVEL == 6:
        buyText = gamebox.from_text(CAMERAWIDTH // 2, 120, "Press 'Space' to buy items!", 32, 'white')
        camera.draw(buyText)

def collision_detection(p_keys):
    """
    Function determines all of the collision detections between gameboxes. Includes
    path-through wall prevention (through checking if the player is above/below the
    wall in the next frame and a buffer), double-jumping if the power-up is taken, spike
    collision (death for player1, tp_to_spawn for player2), player collisions with one
    another "bouncing" off, and regular wall collision for each wall.
    :param p_keys: Keys being pressed
    """
    global LIVES
    global JUMPHEIGHT, canJump, doubleJumpGet, jumpCooldown

    for wall in walls:  # collision detection of character contact with each wall
        if player1.touches(wall):  # any touch
            player1.move_to_stop_overlapping(wall)

        if player2.touches(wall):
            player2.move_to_stop_overlapping(wall)


        # PASS-THROUGH-WALL PREVENTION
        # had to rework this twice, yspeed * 1 was only current frame
        # also me stupid and made p2 yspeed real weird formula-wise was opposite of p1

        if player1.bottom_touches(wall, player1.yspeed * 2) and GRAVITY > 0:  # Prevents going through wall
            if player1.y + player1.yspeed * 2 > wall.y:  # Check if next frame player1 y > wall y
                # print("BOOP") # testing
                player1.y = wall.y - player1.yspeed
                player1.yspeed = 0
                player1.move_to_stop_overlapping(wall)

        if player2.top_touches(wall, player2.yspeed * 2) and GRAVITY > 0: # WORKS
            if player2.y - player2.yspeed * 2 < wall.y: #5/5/21 5:23PM
                # print("BOOP")
                player2.y = wall.y + player2.yspeed
                player2.yspeed = 0
                player2.move_to_stop_overlapping(wall)

        if player1.top_touches(wall, -player1.yspeed * 2) and GRAVITY < 0: # Works (5:33PM)
            if player1.y + player1.yspeed * 2 < wall.y:
                # print("BOOP")
                player1.y = wall.y - player1.yspeed
                player1.yspeed = 0
                player1.move_to_stop_overlapping(wall)

        if player2.bottom_touches(wall, -player2.yspeed * 2) and GRAVITY < 0: # WORKS
            if player2.y - player2.yspeed * 2 > wall.y:
                # print("BOOP")
                player2.y = wall.y + player2.yspeed
                player2.yspeed = 0
                player2.move_to_stop_overlapping(wall)

        # SPIKE COLLISION
        if player1.touches(spikes, 0, -10): # Buffer b/c spike sprite has 10 pixels of whitespace
            LIVES -= 1
            tp_to_spawn(player1)
        if player2.touches(spikes, 0, -10):
            tp_to_spawn(player2)

        # REGULAR JUMPING & DOUBLE JUMPING (FIXED 5/6/21 1:49PM)
        if GRAVITY > 0:
            if player1.bottom_touches(wall):
                player1.yspeed = 0
                canJump = 1
                jumpCooldown = 10 # Constantly set jumpCD because the else includes all other walls.
                if pygame.K_UP in p_keys:
                    player1.yspeed = -JUMPHEIGHT

            else: #BUG FIX: not player1.bottom_touches wall would include ALL other
                # walls because this is in a for loop. Thus, I have to use an else clause.
                jumpCooldown -= 1/len(walls)
                #Since this is in a for loop, it's calling ticks_per_second * len(walls) times

                if doubleJumpGet == 1 and canJump == 1 and jumpCooldown < 0:
                    if pygame.K_UP in p_keys:
                        player1.yspeed = -JUMPHEIGHT  # for smoother jumping
                        jumpCooldown = 35
                        canJump = 0

            if player2.top_touches(wall):
                player2.yspeed = 0
                if pygame.K_w in p_keys:
                    player2.yspeed = -JUMPHEIGHT

        elif GRAVITY < 0:
            if player1.top_touches(wall):
                player1.yspeed = 0
                canJump = 1
                jumpCooldown = 10 # Constantly set jumpCD because the else includes all other walls.
                if pygame.K_UP in p_keys:
                    player1.yspeed = JUMPHEIGHT
            else:
                jumpCooldown -= 1 / len(walls)
                if doubleJumpGet == 1 and canJump == 1 and jumpCooldown < 0:
                    if pygame.K_UP in p_keys:
                        player1.yspeed = JUMPHEIGHT  # for smoother jumping
                        jumpCooldown = 35
                        canJump = 0

            if player2.bottom_touches(wall):
                player2.yspeed = 0
                if pygame.K_w in p_keys:
                    player2.yspeed = JUMPHEIGHT

        # print(jumpCooldown)

        # PLAYER COLLISION DETECTION
        if (player1.bottom_touches(player2) and player2.top_touches(player1)) or \
                (player1.top_touches(player2) and player2.bottom_touches(player1)):
            player1.move_both_to_stop_overlapping(player2)
            if player1.x > player2.x:
                player1.x = player1.x + 3
                player2.x = player2.x - 3
            else:
                player1.x = player1.x - 3
                player2.x = player2.x + 3

        # BOSS COLLISION DETECTION
        if boss.bottom_touches(wall):
            boss.yspeed = 0

        if boss.touches(wall, -10):
            boss.move_to_stop_overlapping(wall, -10)

        camera.draw(wall)


def generate_coin(amount):
    """
    Generates given number of coins and appends them to a list of coins.
    :param amount: Parameter signifying # of coins to be generated.
    """
    global genCoin
    for number in range(0, amount):
        coin = gamebox.from_color(random.randint(100, 750), random.randint(200, 500), "yellow", 5, 5)
        genCoin.append(coin)

def restart_button():
    """
    This function draws the restart button.
    """
    restart_button = gamebox.from_image(CAMERAWIDTH // 2 + 12, 360, "restart_button.png")
    restart_button.scale_by(.7)
    camera.draw(restart_button)

    x, y = camera.mouse
    if restart_button.contains(x, y):
        restart_button.full_size()
        restart_button.scale_by(.8)
        camera.draw(restart_button)
        if camera.mouseclick:
            if GRAVITY < 0:  # Fixes sprite orientation if GAME OVER while gravity flipped
                player1.flip(), player2.flip()
                player1.rotate(180), player2.rotate(180)
            restart()

def level_check(p_keys):
    """
    This function draws each level and its components and mechanics. Walking on pressure
    plates will remove the corresponding gates. This function mostly appends gamebox
    platforms to a list of walls. Walls are cleared and appended each tick to prevent
    lag (must be called per tick to update things like animations, text, and plates).
    :param p_keys: Keys being pressed.
    """
    global LEVEL, walls, door, DO_ONCE, spikes, PAUSE, closeFrame, SPEED, LIVES
    global P2ALIVE, SLOWFALL, GETGUN, NPC1GIFT, showText, SAVELEVEL, gravityCooldown
    global KEYGET, movingPlatformCounter, platformXChange, bossFlipGravity, GRAVITY
    global bossLives, magikoopaFrame, magikoopaFrameCounter, startBossAnimation
    global bossGravityFlipSpeed, bossDirection, platform10Change, moving10PlatformCounter

    roof = gamebox.from_color(400, 10, wallcolor, 800, 40)
    # DOOR (NEXT LEVEL) ACCESS
    if player1.touches(door) and pygame.K_UP in p_keys and isinstance(LEVEL, int):
        LEVEL += 1
        P2ALIVE = 1
        tp_to_spawn(player1)
        tp_to_spawn(player2)

    if LEVEL == 1:
        instruction1 = gamebox.from_text(CAMERAWIDTH // 2, 100, "Press 'G' to flip gravity!", 32, 'white')
        camera.draw(instruction1)
        walls.clear()
        walls.append(gamebox.from_color(275, 500, wallcolor, 550, 20))
        walls.append(gamebox.from_color(300, 285, wallcolor, 700, 20))
        walls.append(gamebox.from_color(700, 400, wallcolor, 300, 20))
        walls.append(gamebox.from_color(400, 10, wallcolor, 800, 40))

        if DO_ONCE == 1:
            generate_coin(10)
            sprite_list.append(spikes)
            DO_ONCE = 0
        spikes.center = [500, 45]
        camera.draw(spikes)

    elif LEVEL == 2:
        spikes.x = 1500
        genCoin.clear()
        walls.clear()
        walls.append(gamebox.from_color(130, 550, wallcolor, 280, 20))
        walls.append(gamebox.from_color(130, 380, wallcolor, 280, 20))
        walls.append(gamebox.from_color(600, 500, wallcolor, 400, 20))
        walls.append(gamebox.from_color(500, 245, wallcolor, 600, 20))
        walls.append(roof)
        door = gamebox.from_image(700, 200, door_sheet[0])

    elif LEVEL == 3:

        if "choco" in showText:
            chocolate.center = [1000, -100]
        else:
            chocolate.center = [400, 220]
        camera.draw(chocolate)
        if player1.touches(chocolate):
            chocolate.center = [1000, -100]
            showText.append("choco")
            SPEED *= 1.5
        walls.clear()
        walls.append(gamebox.from_color(130, 550, wallcolor, 280, 20))
        walls.append(gamebox.from_color(130, 425, wallcolor, 280, 20))
        walls.append(gamebox.from_color(130, 300, wallcolor, 280, 20))
        walls.append(roof)
        walls.append(gamebox.from_color(650, 495, wallcolor, 300, 20))
        walls.append(gamebox.from_color(400, 500, wallcolor, 40, 500))
        door.center = [700, 450]

    elif LEVEL == 4:
        spikes.x = 1000
        walls.clear()
        walls.append(gamebox.from_color(150, 540, wallcolor, 300, 20))
        walls.append(gamebox.from_color(130, 400, wallcolor, 280, 20))
        walls.append(gamebox.from_color(130, 320, wallcolor, 30, 150))
        walls.append(gamebox.from_color(400, 300, wallcolor, 20, 350))
        walls.append(gamebox.from_color(340, 0, wallcolor, 680, 40))  # roof
        walls.append(gamebox.from_color(400, 120, wallcolor, 400, 20))
        walls.append(gamebox.from_color(680, 225, wallcolor, 20, 450))  # right side
        walls.append(gamebox.from_color(675, 525, wallcolor, 250, 20))
        # FIRST USAGE OF PRESSURE PLATE/GATE MECHANIC, COPIED IN LATER LEVELS
        gate = gamebox.from_color(400, 65, 'white', 20, 90)
        walls.append(gate)
        pressureplate = gamebox.from_color(60, 385, 'white', 40, 10)
        walls.append(pressureplate)
        pressureplate2 = gamebox.from_color(525, 25, 'white', 40, 10)
        walls.append(pressureplate2)
        if player1.touches(pressureplate) or player2.touches(pressureplate):
            walls.remove(pressureplate)
            if gate in walls:
                walls.remove(gate)
        if player1.touches(pressureplate2) or player2.touches(pressureplate2):
            walls.remove(pressureplate2)
            if gate in walls:
                walls.remove(gate)

        shopText = gamebox.from_text(700, 500, "Shop ->", 36, "yellow")
        camera.draw(shopText)
        door.center = [780, 485]

    elif LEVEL == 'Game Over': # Clear all objects, paste screen with game over & restart
        walls.clear()
        genCoin.clear()
        camera.clear("black")
        camera.draw(introBackground)
        camera.draw(game_over_screen)

        restart_button()

    elif LEVEL == 'Help':
        PAUSE = 1
        draw_help_screen()
        pause_game()
        closeButton = gamebox.from_image(50, 120, close_sprite_sheet[closeFrame])
        closeButton.scale_by(.75)
        mousex, mousey = camera.mouse
        if closeButton.contains(mousex, mousey):
            closeFrame = 1
            camera.draw(closeButton)
            if camera.mouseclick:
                PAUSE = 0
                LEVEL = SAVELEVEL
                closeFrame = 0
        else:
            closeFrame = 0
            camera.draw(closeButton)

    elif LEVEL == 5:
        spikes.x = 500
        camera.draw(spikes)

        walls.clear()
        walls.append(gamebox.from_color(300, 590, wallcolor, 600, 40))
        walls.append(gamebox.from_color(300, 10, wallcolor, 600, 40))
        walls.append(gamebox.from_color(690, 440, wallcolor, 90, 20))
        walls.append(gamebox.from_color(165, 310, wallcolor, 30, 350))
        walls.append(gamebox.from_color(350, 120, wallcolor, 400, 30))
        walls.append(gamebox.from_color(535, 350, wallcolor, 30, 150))
        walls.append(gamebox.from_color(350, 260, wallcolor, 400, 30))
        walls.append(gamebox.from_color(270, 380, wallcolor, 200, 30))
        door.center = [1000, 800]
        npc1.center = [400, 550]
        camera.draw(npc1)
        camera.draw(gun)
        camera.draw(shop_sign)

        if NPC1GIFT == 0:
            feather_sprite.center = [1000, 700]
        elif NPC1GIFT == 1:
            feather_sprite.center = [200, 540]

            if player1.touches(feather_sprite):
                SLOWFALL = 1
                feather_sprite.center = [1000, 700]
                NPC1GIFT = 2
                showText.append("feather")

        if NPC1GIFT >= 1:
            door.center = [250, 215]
            shop_sign.center = [250, 175]
        camera.draw(feather_sprite)

        if player1.touches(gun) or player2.touches(gun):
            GETGUN = 1
            gun.center = [1200, 700]
            generate_coin(20)

        gate = gamebox.from_color(500, 187, 'white', 20, 120)
        walls.append(gate)
        gate2 = gamebox.from_color(590, 300, 'white', 80, 20)
        walls.append(gate2)
        pressureplate = gamebox.from_color(220, 360, 'white', 40, 10)
        walls.append(pressureplate)
        pressureplate2 = gamebox.from_color(350, 30, 'white', 40, 10)
        walls.append(pressureplate2)
        if player1.touches(pressureplate) or player2.touches(pressureplate):
            walls.remove(pressureplate)
            if gate in walls:
                walls.remove(gate)
            if gate2 in walls:
                walls.remove(gate2)
        if player1.touches(pressureplate2) or player2.touches(pressureplate2):
            walls.remove(pressureplate2)
            if gate in walls:
                walls.remove(gate)
            if gate2 in walls:
                walls.remove(gate2)

    elif LEVEL == 6: # SHOP LEVEL
        walls.clear()
        genCoin.clear()
        spikes.x = 2000

        # Have to do this for restart() to work with my text
        if ringGet == 1:
            ring_sprite.center = [600, 550]
        else:
            ring_sprite.center = [2000, 2000]
        if doubleJumpGet == 0:
            double_jump.center = [450, 550]
        else:
            double_jump.center = [2000, 2000]
        if extraLifeGet == 0:
            extra_life.center = [300, 550]
        else:
            extra_life.center = [2000, 200]

        camera.draw(ring_sprite)
        camera.draw(double_jump)
        camera.draw(extra_life)
        shop_sign.center = [1000, 1000]
        door.center = [750, 538]
        walls.append(roof)
        walls.append(gamebox.from_color(400, 590, wallcolor, 800, 40)) # Floor

    elif LEVEL == 7:
        camera.draw(key_sprite)

        spikes.center = [1000, 2000]

        walls.clear()
        walls.append(gamebox.from_color(100, 400, wallcolor, 200, 30))
        walls.append(gamebox.from_color(100, 590, wallcolor, 200, 30)) # Floor
        walls.append(gamebox.from_color(350, 440, wallcolor, 50, 20))
        walls.append(gamebox.from_color(550, 240, wallcolor, 50, 20))
        walls.append(gamebox.from_color(700, 10, wallcolor, 200, 40)) # right roof
        walls.append(gamebox.from_color(80, 10, wallcolor, 160, 40)) # left roof

        # gate = gamebox.from_color(300, 65, 'white', 200, 30)
        # walls.append(gate)

        gate2 = gamebox.from_color(300, 585, 'white', 200, 30)

        gateCage1 = gamebox.from_color(180, 335, 'white', 20, 100)
        gateCage2 = gamebox.from_color(85, 295, 'white', 160, 20)
        walls.append(gateCage1)
        walls.append(gateCage2)

        pressureplate = gamebox.from_color(655, 35, 'white', 40, 10)
        walls.append(pressureplate)

        if player1.touches(pressureplate) or player2.touches(pressureplate):
            walls.remove(pressureplate)
            walls.append(gate2)
            if gateCage1 in walls:
                walls.remove(gateCage1)
                walls.remove(gateCage2)
        else:
            if gate2 in walls:
                walls.remove(gate2)

        gateBlue = gamebox.from_color(530, 15, 'blue', 150, 30)
        walls.append(gateBlue)

        gateBlueCage = gamebox.from_color(148, 80, 'blue', 20, 100)
        walls.append(gateBlueCage)
        gateBlueCage2 = gamebox.from_color(80, 125, 'blue', 150, 20)
        walls.append(gateBlueCage2)

        pressureplateBlue1 = gamebox.from_color(60, 385, 'blue', 40, 10)
        walls.append(pressureplateBlue1)

        if player1.touches(pressureplateBlue1) or player2.touches(pressureplateBlue1):
            walls.remove(pressureplateBlue1)
            if gateBlue in walls:
                walls.remove(gateBlue)
                walls.remove(gateBlueCage)
                walls.remove(gateBlueCage2)

        walls.append(gamebox.from_color(320, 120, wallcolor, 50, 20))

        if player1.touches(key_sprite) or player2.touches(key_sprite):
            KEYGET = 1
            key_sprite.center = [2000, 2000]
        if KEYGET == 0:
            key_sprite.center = [110, 50]
            door.center = [1000, 2000]
        else:
            key_sprite.center = [2000, 2000]
            door.center = [150, 545]



    elif LEVEL == 8:
        walls.clear()
        spikes.center = [1000, 2000]
        walls.append(gamebox.from_color(100, 400, wallcolor, 200, 30))
        walls.append(gamebox.from_color(200, 270, wallcolor, 120, 25))
        walls.append(gamebox.from_color(100, 590, wallcolor, 200, 30))  # Floor


        if player1.touches(key_sprite) or player2.touches(key_sprite):
            KEYGET = 2


        if KEYGET == 2:
            door.center = [150, 545]
            key_sprite.center = [2000, 2000]
        else:
            door.center = [1000, 2000]
            key_sprite.center = [770, 540]
        camera.draw(key_sprite)

        gateWhite = gamebox.from_color(100, 150, 'white', 200, 30)
        gateWhiteA = gamebox.from_color(650, 590, 'white', 300, 30)
        #gateWhite2 = gamebox.from_color(300, 400, 'white', 200, 30)
        gateWhite3 = gamebox.from_color(600, 100, 'white', 200, 30)
        walls.append(gateWhite)
        walls.append(gateWhiteA)
        #walls.append(gateWhite2)
        walls.append(gateWhite3)

        pressureplate = gamebox.from_color(60, 385, 'white', 40, 10)
        walls.append(pressureplate)

        if player1.touches(pressureplate) or player2.touches(pressureplate):
            walls.remove(pressureplate)
            if gateWhiteA in walls:
                walls.remove(gateWhite)
                walls.remove(gateWhiteA)
        else:
            if gateWhite3 in walls:
                #walls.remove(gateWhite2)
                walls.remove(gateWhite3)

        gateBlue = gamebox.from_color(400, 15, 'blue', 800, 30)
        walls.append(gateBlue)

        gateBlueCage = gamebox.from_color(650, 490, 'blue', 300, 20)
        #gateBlueCage2 = gamebox.from_color(510, 525, 'blue', 10, 100)
        walls.append(gateBlueCage)
        #walls.append(gateBlueCage2)

        pressureplateBlue1 = gamebox.from_color(600, 120, 'blue', 40, 10)
        walls.append(pressureplateBlue1)

        pressureplateBlue2 = gamebox.from_color(120, 170, 'blue', 40, 10)
        walls.append(pressureplateBlue2)
        if player1.touches(pressureplateBlue1) or player2.touches(pressureplateBlue1):
            walls.remove(pressureplateBlue1)
            if gateBlue in walls:
                walls.remove(gateBlue)

                walls.remove(gateBlueCage)
                #walls.remove(gateBlueCage2)

        if player1.touches(pressureplateBlue2) or player2.touches(pressureplateBlue2):
            walls.remove(pressureplateBlue2)
            if gateBlue in walls:
                walls.remove(gateBlue)
                walls.remove(gateBlueCage)
                #walls.remove(gateBlueCage2)

    elif LEVEL == 9:
        spikes.center = [2000, 2000]
        walls.clear()
        walls.append(gamebox.from_color(100, 400, wallcolor, 200, 30))
        walls.append(gamebox.from_color(100, 590, wallcolor, 200, 30))  # Floor
        walls.append(gamebox.from_color(700, 590, wallcolor, 200, 30))  # Floor
        movingPlatform = gamebox.from_color(250 + platformXChange, 400, wallcolor, 120, 25)
        movingPlatform2 = gamebox.from_color(550 - platformXChange, 200, wallcolor, 120, 25)
        movingPlatform3 = gamebox.from_color(250 + platformXChange, 10, wallcolor, 120, 25)
        if movingPlatformCounter == 1:
            platformXChange -= 5
            if player1.touches(movingPlatform): # Has to be separate or both would move ;-;
                player1.x -= 5
            if player2.touches(movingPlatform):
                player2.x -= 5
            if player1.touches(movingPlatform2):
                player1.x += 5
            if player2.touches(movingPlatform2):
                player2.x += 5
            if player1.touches(movingPlatform3):
                player1.x -= 5
            if player2.touches(movingPlatform3):
                player2.x -= 5
        if movingPlatformCounter == 0:
            platformXChange += 5
            if player1.touches(movingPlatform):
                player1.x += 5
            if player2.touches(movingPlatform):
                player2.x += 5
            if player1.touches(movingPlatform2):
                player1.x -= 5
            if player2.touches(movingPlatform2):
                player2.x -= 5
            if player1.touches(movingPlatform3):
                player1.x += 5
            if player2.touches(movingPlatform3):
                player2.x += 5

        if movingPlatform.x == 650:
            movingPlatformCounter = 1

        if movingPlatform.x == 250:
            movingPlatformCounter = 0

        if player1.touches(key_sprite) or player2.touches(key_sprite):
            KEYGET = 3
            generate_coin(10)

        if KEYGET == 3:
            door.center = [750, 545]
            key_sprite.center = [2000, 2000]
        else:
            door.center = [1000, 2000]
            key_sprite.center = [250, 40]
        camera.draw(key_sprite)

        walls.append(movingPlatform)
        walls.append(movingPlatform2)
        walls.append(movingPlatform3)

        gateCage1 = gamebox.from_color(160, 45, 'white', 20, 100)
        gateCage2 = gamebox.from_color(250, 85, 'white', 160, 20)
        gateCage3 = gamebox.from_color(340, 45, 'white', 20, 100)
        walls.append(gateCage1)
        walls.append(gateCage2)
        walls.append(gateCage3)

        pressureplate = gamebox.from_color(105, 380, 'white', 40, 10)
        walls.append(pressureplate)

        if player1.touches(pressureplate) or player2.touches(pressureplate):
            walls.remove(pressureplate)
            if gateCage1 in walls:
                walls.remove(gateCage1)
                walls.remove(gateCage2)
                walls.remove(gateCage3)

    elif LEVEL == 10:
        walls.clear()
        genCoin.clear()
        door.center = [2000, 2000]
        spikes.center = [2000, 2000]
        bossSpikes.center = [700, 560]
        bossSpikes2.center = [150, 370]
        walls.append(gamebox.from_color(100, 400, wallcolor, 200, 30))
        walls.append(gamebox.from_color(100, 590, wallcolor, 200, 30))  # Floor
        walls.append(gamebox.from_color(700, 590, wallcolor, 200, 30))  # Floor

        movingPlatform = gamebox.from_color(220 + platform10Change, 400, wallcolor, 120, 25)
        walls.append(movingPlatform)
        movingPlatform2 = gamebox.from_color(550, 200 + platform10Change//2, wallcolor, 120, 25)
        walls.append(movingPlatform2)

        if moving10PlatformCounter == 1:
            platform10Change -= 5
            if player1.touches(movingPlatform): # Has to be separate or both would move ;-;
                player1.x -= 5
            if player2.touches(movingPlatform):
                player2.x -= 5
            if player1.touches(movingPlatform2):
                player1.y -= 5
            if player2.touches(movingPlatform2):
                player2.y -= 5

        if moving10PlatformCounter == 0:
            platform10Change += 5
            if player1.touches(movingPlatform):
                player1.x += 5
            if player2.touches(movingPlatform):
                player2.x += 5
            if player1.bottom_touches(movingPlatform2, 10):
                player1.y += 5
            if player2.bottom_touches(movingPlatform2, 10):
                player2.y += 5

        if movingPlatform.x == 500:
            moving10PlatformCounter = 1

        if movingPlatform.x == 250:
            moving10PlatformCounter = 0

        camera.draw(movingPlatform)

        pressureplate = gamebox.from_color(60, 385, 'white', 40, 10)
        walls.append(pressureplate)
        BossPlatform1 = gamebox.from_color(700, 180, 'white', 200, 25)
        walls.append(BossPlatform1)

        if player1.touches(pressureplate) or player2.touches(pressureplate):
            walls.remove(pressureplate)
            if BossPlatform1 in walls:
                walls.remove(BossPlatform1)

        BossPlatform2 = gamebox.from_color(125, 180, 'blue', 250, 25)
        walls.append(BossPlatform2)
        pressureplateBlue = gamebox.from_color(760, 160, 'blue', 40, 10)
        walls.append(pressureplateBlue)

        if player1.touches(pressureplateBlue) or player2.touches(pressureplateBlue):
            walls.remove(pressureplateBlue)
            if BossPlatform2 in walls:
                walls.remove(BossPlatform2)

        BossPlatform3 = gamebox.from_color(400, 595, 'orange', 80, 10)
        walls.append(BossPlatform3)
        pressureplateOrange = gamebox.from_color(60, 165, 'orange', 40, 10)
        walls.append(pressureplateOrange)

        if player1.touches(pressureplateOrange) or player2.touches(pressureplateOrange):
            walls.remove(pressureplateOrange)
            if BossPlatform3 in walls:
                walls.remove(BossPlatform3)

        bossFlipGravity += 1
        if bossLives > 1:
            bossGravityFlipSpeed = 1
            if bossFlipGravity % 300 == 0: # Every 6 seconds, boss will flip gravity
                GRAVITY *= -1
                player1.flip(), player1.rotate(180)
                player2.flip(), player2.rotate(180)

            if bossFlipGravity % 300 == 250: # Fit sprite animation to flipping gravity
                startBossAnimation = 1

        if bossLives == 1: # Double speed because one life left
            bossGravityFlipSpeed = 2
            if bossFlipGravity % 150 == 0:  # Every 3 seconds, boss will flip gravity
                GRAVITY *= -1
                player1.flip(), player1.rotate(180)
                player2.flip(), player2.rotate(180)
            if bossFlipGravity % 150 == 125:
                startBossAnimation = 1

        #BOSS ANIMATION
        boss.image = magikoopa_sprite_sheet[magikoopaFrame]
        if startBossAnimation == 1:
            magikoopaFrameCounter += 1
            if magikoopaFrameCounter % (4//bossGravityFlipSpeed) == 0:
                magikoopaFrame += 1
                if magikoopaFrame >= 16:
                    magikoopaFrame = 0
                    startBossAnimation = 0

        bossText = gamebox.from_text(400, 80, "Watch out! The boss can flip gravity too!", 32, "white")
        camera.draw(bossText)
        if boss.touches(bossSpikes):
            bossLives -= 1
            boss.center = [140, 133]
            boss.flip()
            bossDirection = "right"
        if boss.touches(bossSpikes2):
            bossLives -= 1
            boss.center = [400, 500]
            boss.flip()
            bossDirection = "left"
        if boss.y > CAMERAHEIGHT + 100:
            bossLives -= 1
        # In LEVEL == 10 statement so players can touch hidden boss sprite and
        # not die
        if player1.touches(boss, -10) or player2.touches(boss, -10):
            tp_to_spawn(player1)
            tp_to_spawn(player2)
            LIVES -= 1

        if player1.touches(bossSpikes, -5) or player2.touches(bossSpikes, -10) or \
            player1.touches(bossSpikes2, -5) or player2.touches(bossSpikes2, -10):
            LIVES -= 1
            tp_to_spawn(player1)
            tp_to_spawn(player2)

        camera.draw(bossSpikes)
        camera.draw(bossSpikes2)
        if bossLives > 0:
            camera.draw(boss)
        else:
            LEVEL = 'Win'

    elif LEVEL == 'Win':
        walls.clear()
        pause_game()
        camera.clear('black')
        camera.draw(introBackground)
        camera.draw(winScreen)
        restart_button()



def restart():
    """
    This function resets all the variables to default when the restart button is pressed.
    """
    global LEVEL, LIVES, SPEED, GRAVITY, door, COINS, DO_ONCE, P2ALIVE, DEFAULTSPEED
    global sprite_direction, character_frame, character_counter
    global doggo_frame, doggo_counter, doggo_direction, doggo_idle_frame, idle_counter
    global NPC1GIFT, SLOWFALL, GETGUN, ringGet, showText, KEYGET, doubleJumpGet
    global extraLifeGet, bossFlipGravity, startBossAnimation, bossLives
    global bossGravityFlipSpeed, platformXChange, bossDirection, platform10Change
    global textCounter, featherCounter, ringCounter, doubleJumpCounter, movingPlatformCounter
    global moving10PlatformCounter

    spikes.center = [1000, 2000]
    bossSpikes.center = [1000, 2000]
    bossSpikes2.center = [1000, 2000]
    boss.center = [700, 133]
    gun.center = [250, 200]
    platformXChange = 5
    platform10Change = 5
    textCounter, featherCounter, ringCounter, doubleJumpCounter = 0, 0, 0, 0
    movingPlatformCounter = 0
    moving10PlatformCounter = 0
    KEYGET = 0
    GETGUN, SLOWFALL, NPC1GIFT = 0, 0, 0
    extraLifeGet = 0
    doubleJumpGet = 0
    ringGet = 1
    if bossDirection == "right":
        boss.flip()

    bossFlipGravity = 0
    startBossAnimation = 0
    bossLives = 3
    bossGravityFlipSpeed = 1

    character_counter = 0
    sprite_direction = "right"
    character_frame = 0
    showText = []

    doggo_counter = 0
    doggo_direction = "right"
    doggo_frame = 0
    doggo_idle_frame = 0
    idle_counter = 0

    LEVEL = 1
    COINS = 0
    LIVES = 3
    SPEED = 8
    GRAVITY = 2
    tp_to_spawn(player1)
    tp_to_spawn(player2)
    door = gamebox.from_image(200, 240, door_sheet[0])
    DO_ONCE = 1
    P2ALIVE = 1



def tp_to_spawn(p_player):
    """
    Teleports player to spawn and resets their speed.
    :param p_player: Given player.
    """
    p_player.x = RESPAWNCOORDS[0]
    p_player.y = RESPAWNCOORDS[1]
    p_player.yspeed = 0

def track_coins():
    """
    This function tracks the coins being collected and removes them if there are coins in
    the list. "if genCoin:" is used to prevent crashing from an empty list.
    # CHANGED TO len(genCoin) != 0 for readability
    """
    global COINS
    for coin in genCoin:
        camera.draw(coin)
        if len(genCoin) != 0:
            if player1.touches(coin):
                genCoin.remove(coin)
                COINS += 1
            if player2.touches(coin):
                genCoin.remove(coin)
                COINS += 1


def tick(keys):
    """
    Main function being called 50 times a second, calls all the other functions of
    the program.
    :param keys: Parameter signifying which keys are being pressed
    """



    camera.clear("black")
    camera.draw(caveBackground)
    camera.draw(door)
    camera.draw(player1)
    camera.draw(player2)

    # print(bossFlipGravity)



    track_coins()
    movement(keys)
    powerups(keys)
    create_text(keys)
    pause_game()
    boundary_action()
    collision_detection(keys)
    level_check(keys)
    player_lives()

    camera.display()  # Draws everything

ticks_per_second = 50 # Variable used quickly change tick setting & for debugging

gamebox.timer_loop(ticks_per_second, tick)
