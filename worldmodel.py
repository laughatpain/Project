from entities import *
import pygame
import ordered_list
from occ_grid import *
import point
import math
import random
import image_store
import save_load


BLOB_RATE_SCALE = 4
BLOB_ANIMATION_RATE_SCALE = 50
BLOB_ANIMATION_MIN = 1
BLOB_ANIMATION_MAX = 3

ORE_CORRUPT_MIN = 20000
ORE_CORRUPT_MAX = 30000

QUAKE_STEPS = 10
QUAKE_DURATION = 1100
QUAKE_ANIMATION_RATE = 100

VEIN_SPAWN_DELAY = 500
VEIN_RATE_MIN = 8000
VEIN_RATE_MAX = 17000

PROPERTY_KEY = 0

BGND_KEY = 'background'
BGND_NUM_PROPERTIES = 4
BGND_NAME = 1
BGND_COL = 2
BGND_ROW = 3

MINER_KEY = 'miner'
MINER_NUM_PROPERTIES = 7
MINER_NAME = 1
MINER_LIMIT = 4
MINER_COL = 2
MINER_ROW = 3
MINER_RATE = 5
MINER_ANIMATION_RATE = 6

OBSTACLE_KEY = 'obstacle'
OBSTACLE_NUM_PROPERTIES = 4
OBSTACLE_NAME = 1
OBSTACLE_COL = 2
OBSTACLE_ROW = 3

ORE_KEY = 'ore'
ORE_NUM_PROPERTIES = 5
ORE_NAME = 1
ORE_COL = 2
ORE_ROW = 3
ORE_RATE = 4

SMITH_KEY = 'blacksmith'
SMITH_NUM_PROPERTIES = 7
SMITH_NAME = 1
SMITH_COL = 2
SMITH_ROW = 3
SMITH_LIMIT = 4
SMITH_RATE = 5
SMITH_REACH = 6

VEIN_KEY = 'vein'
VEIN_NUM_PROPERTIES = 6
VEIN_NAME = 1
VEIN_RATE = 4
VEIN_COL = 2
VEIN_ROW = 3
VEIN_REACH = 5

class WorldModel:
   def __init__(self, num_rows, num_cols, background):
      self.background = Grid(num_cols, num_rows, background)
      self.num_rows = num_rows
      self.num_cols = num_cols
      self.occupancy = Grid(num_cols, num_rows, None)
      self.entities = []
      self.action_queue = ordered_list.OrderedList()

   def within_bounds(self, pt):
      return (pt.x >= 0 and pt.x < self.num_cols and
         pt.y >= 0 and pt.y < self.num_rows)

   def find_nearest(self, pt, type):
      oftype = [(e, distance_sq(pt, e.get_position()))
         for e in self.entities if isinstance(e, type)]

      return nearest_entity(oftype)

   def is_occupied(self, pt):
      return (self.within_bounds(pt) and
         self.occupancy.get_cell(pt) != None)

   def add_entity(self, entity):
      pt = entity.get_position()
      if self.within_bounds(pt):
         old_entity = self.occupancy.get_cell(pt)
         if old_entity != None:
            clear_pending_actions(old_entity)
         self.occupancy.set_cell(pt, entity)
         self.entities.append(entity)

   def move_entity(self, entity, pt):
      tiles = []
      if self.within_bounds(pt):
         old_pt = entity.get_position()
         self.occupancy.set_cell(old_pt, None)
         tiles.append(old_pt)
         self.occupancy.set_cell(pt, entity)
         tiles.append(pt)
         entity.set_position(pt)

      return tiles

   def remove_entity(self, entity):
      self.remove_entity_at(entity.get_position())

   def remove_entity_at(self, pt):
      if (self.within_bounds(pt) and
         self.occupancy.get_cell(pt) != None):
         entity =self.occupancy.get_cell(pt)
         entity.set_position(point.Point(-1, -1))
         self.entities.remove(entity)
         self.occupancy.set_cell(pt, None)

   def schedule_action(self, action, time):
      self.action_queue.insert(action, time)


   def unschedule_action(self, action):
      self.action_queue.remove(action)

   def update_on_time(self, ticks):
      tiles = []

      next = self.action_queue.head()
      while next and next.ord < ticks:
         self.action_queue.pop()
         tiles.extend(next.item(ticks))  # invoke action function
         next = self.action_queue.head()

      return tiles

   def get_background_image(self, pt):
      if self.within_bounds(pt):
         return get_image(self.background.get_cell(pt))


   def get_background(self, pt):
      if self.within_bounds(pt):
         return self.background.get_cell(pt)


   def set_background(self, pt, bgnd):
      if self.within_bounds (pt):
         self.background.set_cell(pt, bgnd)


   def get_tile_occupant(self, pt):
      if self.within_bounds(pt):
         return self.occupancy.get_cell(pt)


   def get_entities(self):
      return self.entities

   def next_position(self, entity_pt, dest_pt):
      horiz = sign(dest_pt.x - entity_pt.x)
      new_pt = point.Point(entity_pt.x + horiz, entity_pt.y)

      if horiz == 0 or self.is_occupied(new_pt):
         vert = sign(dest_pt.y - entity_pt.y)
         new_pt = point.Point(entity_pt.x, entity_pt.y + vert)

         if vert == 0 or self.is_occupied(new_pt):
            new_pt = point.Point(entity_pt.x, entity_pt.y)

      return new_pt

   def blob_next_position(self, entity_pt, dest_pt):
      horiz = sign(dest_pt.x - entity_pt.x)
      new_pt = point.Point(entity_pt.x + horiz, entity_pt.y)

      if horiz == 0 or (self.is_occupied(new_pt) and
         not isinstance(self.get_tile_occupant(new_pt),
         Ore)):
         vert = sign(dest_pt.y - entity_pt.y)
         new_pt = point.Point(entity_pt.x, entity_pt.y + vert)

         if vert == 0 or (self.is_occupied(new_pt) and
            not isinstance(self.get_tile_occupant(new_pt),
            Ore)):
            new_pt = point.Point(entity_pt.x, entity_pt.y)

      return new_pt

   def create_miner_not_full_action(self, entity, i_store):
      def action(current_ticks):
         entity.remove_pending_action(action)

         entity_pt = entity.get_position()
         ore = self.find_nearest(entity_pt, Ore)
         (tiles, found) = entity.miner_to_ore(self, ore)

         new_entity = entity
         if found:
            new_entity = self.try_transform_miner(entity,
               self.try_transform_miner_not_full)

         self.schedule_action_2(new_entity,
            self.create_miner_action(new_entity, i_store),
            current_ticks + new_entity.get_rate())
         return tiles
      return action

   def create_miner_full_action(self, entity, i_store):
      def action(current_ticks):
         entity.remove_pending_action(action)

         entity_pt = entity.get_position()
         smith = self.find_nearest(entity_pt, Blacksmith)
         (tiles, found) = entity.miner_to_smith(self, smith)

         new_entity = entity
         if found:
            new_entity = self.try_transform_miner(entity,
               self.try_transform_miner_full)

         self.schedule_action_2(new_entity,
            self.create_miner_action(new_entity, i_store),
            current_ticks + new_entity.get_rate())
         return tiles
      return action

   def create_miner_action(self, entity, image_store):
      if isinstance(entity, MinerNotFull):
         return self.create_miner_not_full_action(entity, image_store)
      else:
         return self.create_miner_full_action(entity, image_store)

   def schedule_miner(self, miner, ticks, i_store):
      self.schedule_action_2(miner, self.create_miner_action(miner, i_store),
         ticks + miner.get_rate())
      self.schedule_animation(miner)

   def schedule_action_2(self, entity, action, time):
      entity.add_pending_action(action)
      self.schedule_action(action, time)


   def schedule_animation(self, entity, repeat_count=0):
      self.schedule_action_2(entity,
         self.create_animation_action(entity, repeat_count),
         entity.get_animation_rate())

   def create_animation_action(self, entity, repeat_count):
      def action(current_ticks):
         entity.remove_pending_action(action)

         entity.next_image()

         if repeat_count != 1:
            self.schedule_action_2(entity,
               self.create_animation_action(entity, max(repeat_count - 1, 0)),
               current_ticks + entity.get_animation_rate())

         return [entity.get_position()]
      return action

   def create_ore_blob_action(self, entity, i_store):
      def action(current_ticks):
         entity.remove_pending_action(action)

         entity_pt = entity.get_position()
         vein = self.find_nearest(entity_pt, Vein)
         (tiles, found) = entity.blob_to_vein(self, vein)

         next_time = current_ticks + entity.get_rate()
         if found:
            quake = self.create_quake(tiles[0], current_ticks, i_store)
            self.add_entity(quake)
            next_time = current_ticks + entity.get_rate() * 2

         self.schedule_action_2(entity,
            self.create_ore_blob_action(entity, i_store),
            next_time)

         return tiles
      return action

   def find_open_around(self, pt, distance):
      for dy in range(-distance, distance + 1):
         for dx in range(-distance, distance + 1):
            new_pt = point.Point(pt.x + dx, pt.y + dy)

            if (self.within_bounds(new_pt) and
               (not self.is_occupied(new_pt))):
               return new_pt

      return None

   def create_vein_action(self, entity, i_store):
      def action(current_ticks):
         entity.remove_pending_action(action)

         open_pt = self.find_open_around(entity.get_position(),
            entity.get_resource_distance())
         if open_pt:
            ore = self.create_ore(
            "ore - " + entity.get_name() + " - " + str(current_ticks),
               open_pt, current_ticks, i_store)
            self.add_entity(ore)
            tiles = [open_pt]
         else:
            tiles = []

         self.schedule_action_2(entity,
            self.create_vein_action(entity, i_store),
            current_ticks + entity.get_rate())
         return tiles
      return action

   def try_transform_miner_full(self, entity):
      new_entity = MinerNotFull(
         entity.get_name(), entity.get_resource_limit(),
         entity.get_position(), entity.get_rate(),
         entity.get_images(), entity.get_animation_rate())

      return new_entity

   def try_transform_miner_not_full(self, entity):
      if entity.resource_count < entity.resource_limit:
         return entity
      else:
         new_entity = MinerFull(
            entity.get_name(), entity.get_resource_limit(),
            entity.get_position(), entity.get_rate(),
            entity.get_images(), entity.get_animation_rate())
         return new_entity

   def try_transform_miner(self, entity, transform):
      new_entity = transform(entity)
      if entity != new_entity:
         self.clear_pending_actions_2(entity)
         self.remove_entity_at(entity.get_position())
         self.add_entity(new_entity)
         self.schedule_animation(new_entity)

      return new_entity

   def create_entity_death_action(self, entity):
      def action(current_ticks):
         entity.remove_pending_action (action)
         pt = entity.get_position()
         self.remove_entity(entity)
         return [pt]
      return action

   def create_ore_transform_action(self, entity, i_store):
      def action(current_ticks):
         entity.remove_pending_action(action)
         blob = self.create_blob(entity.get_name() + " -- blob",
            entity.get_position(),
            entity.get_rate() // BLOB_RATE_SCALE,
            current_ticks, i_store)

         self.remove_entity(entity)
         self.add_entity(blob)

         return [blob.get_position()]
      return action

   def remove_entity_2(self, entity):
      for action in entity.get_pending_actions():
         self.unschedule_action(action)
      entity.clear_pending_actions()
      self.remove_entity(entity)

   def create_blob(self, name, pt, rate, ticks, i_store):
      blob = OreBlob(name, pt, rate,
         image_store.get_images(i_store, 'blob'),
         random.randint(BLOB_ANIMATION_MIN, BLOB_ANIMATION_MAX)
         * BLOB_ANIMATION_RATE_SCALE)
      self.schedule_blob(blob, ticks, i_store)
      return blob

   def schedule_blob(self, blob, ticks, i_store):
      self.schedule_action_2(blob, self.create_ore_blob_action (blob, i_store),
         ticks + blob.get_rate())
      self.schedule_animation(blob)

   def create_ore(self, name, pt, ticks, i_store):
      ore = Ore(name, pt, image_store.get_images(i_store, 'ore'),
         random.randint(ORE_CORRUPT_MIN, ORE_CORRUPT_MAX))
      self.schedule_ore(ore, ticks, i_store)

      return ore

   def schedule_ore(self, ore, ticks, i_store):
       self.schedule_action_2(ore,
         self.create_ore_transform_action(ore, i_store),
         ticks + ore.get_rate())

   def create_quake(self, pt, ticks, i_store):
      quake = Quake("quake", pt,
         image_store.get_images(i_store, 'quake'), QUAKE_ANIMATION_RATE)
      self.schedule_quake(quake, ticks)
      return quake

   def schedule_quake(self, quake, ticks):
      self.schedule_animation(quake, QUAKE_STEPS)
      self.schedule_action_2(quake, self.create_entity_death_action(quake),
         ticks + QUAKE_DURATION)

   def create_vein(self, name, pt, ticks, i_store):
      vein = Vein("vein" + name,
         random.randint(VEIN_RATE_MIN, VEIN_RATE_MAX),
         pt, image_store.get_images(i_store, 'vein'))
      return vein

   def schedule_vein(self, vein, ticks, i_store):
      self.schedule_action_2(vein, self.create_vein_action(vein, i_store),
         ticks + vein.get_rate())

   def clear_pending_actions_2(self,entity):
      for action in entity.get_pending_actions():
         self.unschedule_action(action)
      entity.clear_pending_actions()

   def save_world(self, file):
      self.save_entities(file)
      self.save_background(file)

   def save_entities(self, file):
      for entity in self.get_entities():
         file.write(entity.entity_string() + '\n')


   def save_background(self, file):
      for row in range(0, self.num_rows):
         for col in range(0, self.num_cols):
            file.write('background ' +
               entities.get_name(
                  self.get_background(point.Point(col, row))) +
               ' ' + str(col) + ' ' + str(row) + '\n')


   def load_world(self, images, file, run=False):
      for line in file:
         properties = line.split()
         if properties:
            if properties[PROPERTY_KEY] == BGND_KEY:
               self.add_background(properties, images)
            else:
               self.add_entity_2(properties, images, run)


   def add_background(self, properties, i_store):
      if len(properties) >= BGND_NUM_PROPERTIES:
         pt = point.Point(int(properties[BGND_COL]), int(properties[BGND_ROW]))
         name = properties[BGND_NAME]
         self.set_background(pt,
            Background(name, image_store.get_images(i_store, name)))


   def add_entity_2(self, properties, i_store, run):
      new_entity = save_load.create_from_properties(properties, i_store)
      if new_entity:
         self.add_entity(new_entity)
         if run:
            self.schedule_entity(new_entity, i_store)

   def schedule_entity(self, entity, i_store):
      if isinstance(entity, MinerNotFull):
         self.schedule_miner(entity, 0, i_store)
      elif isinstance(entity, Vein):
         self.schedule_vein(entity, 0, i_store)
      elif isinstance(entity, Ore):
         self.schedule_ore(entity, 0, i_store)

   def on_keydown_2(self, event, entity_select, i_store):
      x_delta = 0
      y_delta = 0
      if event.key == pygame.K_UP: y_delta -= 1
      if event.key == pygame.K_DOWN: y_delta += 1
      if event.key == pygame.K_LEFT: x_delta -= 1
      if event.key == pygame.K_RIGHT: x_delta += 1
      elif event.key in keys.ENTITY_KEYS:
         entity_select = keys.ENTITY_KEYS[event.key]
      elif event.key == keys.SAVE_KEY: self.save_world(WORLD_FILE_NAME)
      elif event.key == keys.LOAD_KEY: self.load_world(i_store, WORLD_FILE_NAME)

      return ((x_delta, y_delta), entity_select)

   def save_world_2(self, filename):
      with open(filename, 'w') as file:
         self.save_world(file)


   def load_world_2(self, i_store, filename):
      with open(filename, 'r') as file:
         self.load_world(i_store, file)


def nearest_entity(entity_dists):
   if len(entity_dists) > 0:
      pair = entity_dists[0]
      for other in entity_dists:
         if other[1] < pair[1]:
            pair = other
      nearest = pair[0]
   else:
      nearest = None

   return nearest


def distance_sq(p1, p2):
   return (p1.x - p2.x)**2 + (p1.y - p2.y)**2

def sign(x):
   if x < 0:
      return -1
   elif x > 0:
      return 1
   else:
      return 0


def adjacent(pt1, pt2):
   return ((pt1.x == pt2.x and abs(pt1.y - pt2.y) == 1) or
      (pt1.y == pt2.y and abs(pt1.x - pt2.x) == 1))
