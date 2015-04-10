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

def activity_loop(view, world, i_store):
   pygame.key.set_repeat(keys.KEY_DELAY, keys.KEY_INTERVAL)

   entity_select = None
   while 1:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            return
         elif event.type == pygame.MOUSEMOTION:
            view.handle_mouse_motion(event)
         elif event.type == pygame.MOUSEBUTTONDOWN:
            tiles = view.handle_mouse_button(world, event, entity_select,
               i_store)
            view.update_view_tiles(tiles)
         elif event.type == pygame.KEYDOWN:
            entity_select = view.handle_keydown_2(event, i_store, world,
               entity_select)




