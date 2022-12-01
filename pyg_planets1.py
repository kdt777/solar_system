# Import a library of functions called 'pygame'
import pygame
from pygame.locals import *
import pygame.freetype
import pygame.gfxdraw

import math
import time
from collections import deque

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (660,40)

# Initialize the game engine
pygame.init()
print ("pygame version:", pygame.__version__)
GAME_FONT = pygame.freetype.Font(None,10)     # ("freesansbold.ttf", 24)

# Define some colors
WHITE    = ( 255, 255, 255)
CREAM    = ( 255, 253, 208)
RED      = ( 255,   0,   0)
ORANGE   = ( 255, 165,   0)
YELLOW   = ( 255, 255,   0)
PARCHMT  = ( 241, 241, 212)
AZURE    = ( 204, 255, 204)
OLIVE    = (  51,  51,   0)
GREEN    = (   0, 255,   0)
GREEN2   = (   0, 220,   0)
BLUE     = (   0,   0, 255)
BLACK    = (   0,   0,   0)

PLANET_NAME = ["Mercury", "Venus", "Earth", "Mars"]
PLANET_COLR = {pname: color for pname, color in zip(PLANET_NAME, (BLACK, ORANGE, BLUE, RED))}
PLANET_SIZE = {pname: size for pname, size in zip(PLANET_NAME, (4.9, 12.1, 12.7, 6.8))}
PLANET_DIST = {pname: d for pname, d in zip(PLANET_NAME, (0.4, 0.7, 1.0, 1.5))}
pl_opey = {pname: PLANET_DIST[pname]**(3.0/2.0) for pname in PLANET_NAME}
print ("Planets:", PLANET_NAME)
print ("  colrs:", PLANET_COLR)
print ("  sizes:", PLANET_SIZE)
print ("   dist:", PLANET_DIST)
print ("orb per:", pl_opey, "earth years")

# Opening and setting the window size
win_width = 650; win_height = 650
win_size = (win_width, win_height)
screen = pygame.display.set_mode(win_size)
Ox = Oy = 325

fineness = 400

# Setting the window title
pygame.display.set_caption("Planets - game speed = 1.0") # + str(gm_speed))
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
print("Clock =", clock) 

def game_loop():

  # Loop until the user clicks the CLOSE or hits ESC.
  game_done = False
  ctr = 0; gm_speed = 1.0

  pl_trail_X = {pname: deque(maxlen=600) for pname in PLANET_NAME + ['Moon']}    # planets' orbit trails - X values
  pl_trail_Y = {pname: deque(maxlen=600) for pname in PLANET_NAME + ['Moon']}    # planets' orbit trails - Y values
  #pl_trail_ctr = 0
  
  while not game_done:
    
    for event in pygame.event.get(): # User did something
      if event.type == pygame.QUIT:   # user clicked close icon
        print("User asked to quit.")
        game_done = True   # Flag that we are done so we exit this loop
      elif event.type == pygame.KEYDOWN:
        print("User pressed key:", event.key)
        kname = pygame.key.name(event.key)
        print("       key name = ", kname) 
        if event.key == K_ESCAPE:     # user pressed escape key
          print("  User pressed ESC.")
          message_display('escape')
          game_done = True
        if event.unicode == '+':    # user pressed '+' key
          print("  User pressed PLUS.")
          gm_speed *= 2; ctr = 0
          message_display('faster')
          pl_trail_X['Moon'].clear(); pl_trail_Y['Moon'].clear()
          pygame.display.set_caption("Planets - game speed = " + str(gm_speed)) 
        if event.unicode == '-':   # user pressed '-' key
          print("  User pressed MINUS.")
          gm_speed /= 2; ctr = 0
          pygame.display.set_caption("Planets - game speed = " + str(gm_speed))
          message_display('slower')
          pl_trail_X['Moon'].clear(); pl_trail_Y['Moon'].clear()
        if event.key == K_p:   # user pressed 'p' key
          print("  User pressed 'p'.")
          message_display('paused')
          pausing() 
 
      # First, clear the screen to white. Don't put other drawing commands
      # above this, or they will be erased with this command.
    screen.fill(AZURE)   #(WHITE)

    pygame.draw.circle(screen, YELLOW, [Ox, Oy], 30, 0)    #draw sun
    
    earthDays = 365.25*ctr*gm_speed/math.pi/2/fineness
    
    for p in PLANET_NAME:     # the 4 planets
      pR = 200.0 * PLANET_DIST[p] 
      pX = pR * math.cos(ctr*gm_speed/fineness/pl_opey[p])
      pY = pR * math.sin(ctr*gm_speed/fineness/pl_opey[p])
      qX = int(Ox + pX)
      qY = int(Oy - pY)
      pygame.draw.circle(screen, PLANET_COLR[p], 
                          [qX, qY], int(PLANET_SIZE[p]), 0)     #draw planet
      if p == "Earth":
        mX = int(Ox + pX + 25 * math.cos(earthDays*math.pi/14.5))
        mY = int(Oy - pY - 25 * math.sin(earthDays*math.pi/14.5))
        pygame.draw.circle(screen, OLIVE, [mX, mY], 3, 0)       #draw moon

      if ctr%20 == 0:   #planet trail
        pl_trail_X[p].append(qX)
        pl_trail_Y[p].append(qY)
        #print("%%%", ctr, len(pl_trail_X[p]))
      if p == "Earth" and ctr%5 == 0:   #moon trail   
        pl_trail_X['Moon'].append(mX)
        pl_trail_Y['Moon'].append(mY)
      if len(pl_trail_X[p]) > 1:
        #print("pl_trail_ctr =", len(pl_trail_X[p])) 
        for tctr in range (len(pl_trail_X[p])):
          pygame.gfxdraw.pixel(screen, pl_trail_X[p][tctr], pl_trail_Y[p][tctr], PLANET_COLR[p])  #draw planet trail

    if len(pl_trail_X['Moon']) > 1:
      for tctr in range (len(pl_trail_X['Moon'])):
        pygame.gfxdraw.pixel(screen, pl_trail_X['Moon'][tctr], pl_trail_Y['Moon'][tctr], OLIVE)   #draw moon trail
       
    GAME_FONT.render_to(screen, (510, 10), "* Mercury", BLACK)
    GAME_FONT.render_to(screen, (520, 20), "* Venus", ORANGE)
    GAME_FONT.render_to(screen, (530, 30), "* Earth", BLUE)
    GAME_FONT.render_to(screen, (540, 40), "* Mars", RED)
    GAME_FONT.render_to(screen, (10, 20), "Press escape key to end game", BLACK)
    GAME_FONT.render_to(screen, (10, 40), "Press + or - to adjust speed", BLACK)
    GAME_FONT.render_to(screen, (10, 60), "Press P to pause play", BLACK)
    GAME_FONT.render_to(screen, (10, 75), "(any key to resume)", BLACK)
    GAME_FONT.render_to(screen, (530, 580), str(int(earthDays))+" earth days", BLUE)

      # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

      # --- Limit to 60 frames per second
    clock.tick(40)

    ctr += 1

  pygame.quit()

  print("ctr =", ctr)
  print("trails...") 
  for p in PLANET_NAME:
    print(p, len(pl_trail_X[p])) 
    #print("   ", len(pl_trail_X[p]), pl_trail_X[p])

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',12)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (580,64)
    screen.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(1)   # seconds

def pausing(): 
  while True:
    clock.tick(1)   # prevents high cpu usage
    for event in pygame.event.get():
      print("   wait for it...") 
      if event.type == QUIT:
          pygame.quit()
      if event.type == KEYDOWN: # and event.key == K_f:
          return    

game_loop()

