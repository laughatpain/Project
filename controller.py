import pygame
import worldmodel
import point

KEY_DELAY = 400
KEY_INTERVAL = 100

TIMER_FREQUENCY = 100

def on_keydown(event):
   x_delta = 0
   y_delta = 0
   if event.key == pygame.K_UP: y_delta -= 1
   if event.key == pygame.K_DOWN: y_delta += 1
   if event.key == pygame.K_LEFT: x_delta -= 1
   if event.key == pygame.K_RIGHT: x_delta += 1

   return (x_delta, y_delta)


def mouse_to_tile(pos, tile_width, tile_height):
   return point.Point(pos[0] // tile_width, pos[1] // tile_height)




