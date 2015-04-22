import point
import image_store

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


class Background:
   def __init__(self, name, imgs):
      self.name = name
      self.imgs = imgs
      self.current_img = 0

class Entity (object):
   def __init__(self, name, position, imgs):
      self.name = name
      self.position = position
      self.imgs = imgs

   def get_name(self):
      return self.name

   def set_position(self, point):
      self.position = point

   def get_position(self):
      return self.position

   def get_images(self):
      return self.imgs

   def get_image(self):
      return self.imgs[self.current_img]

class PendingAction (Entity):
   def __init__ (self, name, position, imgs):
      self.name = name
      self.position = position
      self.imgs = imgs
      super(PendingAction, self).__init__ (name, position, imgs)
   def remove_pending_action(self, action):
         self.pending_actions.remove(action)

   def add_pending_action(self, action):
      self.pending_actions.append(action)


   def get_pending_actions(self):
         return self.pending_actions

   def clear_pending_actions(self):
         self.pending_actions = []

class Moving (PendingAction):
   def __init__ (self, name, position, imgs, animation_rate):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.animation_rate = animation_rate
      super(Moving, self).__init__ (name, position, imgs)

   def get_animation_rate(self):
      return self.animation_rate

   def schedule_action(self, world, action, time):
      self.add_pending_action(action)
      world.schedule_action(action, time)


   def schedule_animation(self, world, repeat_count=0):
      self.schedule_action(world,
         self.create_animation_action(world, repeat_count),
         self.get_animation_rate())

   def next_image(self):
      self.current_img = (self.current_img + 1) % len(self.imgs)

   def create_animation_action(self, world, repeat_count):
      def action(current_ticks):
         self.remove_pending_action(action)

         self.next_image()

         if repeat_count != 1:
            self.schedule_action(world,
               self.create_animation_action(world, max(repeat_count - 1, 0)),
               current_ticks + self.get_animation_rate())

         return [self.get_position()]
      return action

class MovingRate (Moving):
   def __init__ (self, name, position, imgs, animation_rate, rate):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.animation_rate = animation_rate
      self.rate = rate
      super(MovingRate, self).__init__ (name, position, imgs, animation_rate)

   def get_rate (self):
      return self.rate


class Miner (MovingRate):
   def __init__ (self, name, position, imgs, animation_rate, rate, resource_limit):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.animation_rate = animation_rate
      self.rate = rate
      self.resource_limit = resource_limit
      super(Miner, self).__init__ (name, position, imgs, animation_rate, rate)

   def set_resource_count(self, n):
      self.resource_count = n

   def get_resource_count(self):
      return self.resource_count

   def get_resource_limit(self):
      return self.resource_limit

   def try_transform_miner(self, world, transform):
      new_entity = transform(world)
      if self != new_entity:
         world.clear_pending_actions(self)
         world.remove_entity_at(self.get_position())
         world.add_entity(new_entity)
         new_entity.schedule_animation(world)

      return new_entity

   def create_miner_action(self, world, image_store):
      if isinstance(self, MinerNotFull):
         return self.create_miner_not_full_action(world, image_store)
      else:
         return self.create_miner_full_action(world, image_store)

class NotAnimated (PendingAction):
   def __init__ (self, name, position, imgs, rate):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.rate = rate
      super(NotAnimated, self).__init__ (name, position, imgs)

   def get_rate (self):
      return self.rate

   def remove_entity(self, world):
      for action in self.get_pending_actions():
         world.unschedule_action(action)
      self.clear_pending_actions()
      world.remove_entity(self)

   def schedule_action(self, world, action, time):
      self.add_pending_action(action)
      world.schedule_action(action, time)



class MinerNotFull (Miner):
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      super(MinerNotFull, self).__init__ (name, position, imgs, animation_rate,
      rate, resource_limit)
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
      self.resource_limit = resource_limit
      self.resource_count = 0
      self.animation_rate = animation_rate
      self.pending_actions = []

   def entity_string(self):
         return ' '.join(['miner', self.name, str(self.position.x),
            str(self.position.y), str(self.resource_limit),
            str(self.rate), str(self.animation_rate)])

   def schedule_miner(self, world, ticks, i_store):
      self.schedule_action(world, self.create_miner_action(world, i_store),
         ticks + self.get_rate())
      self.schedule_animation(world)

   def miner_to_ore(self, world, ore):
      entity_pt = self.get_position()
      if not ore:
         return ([entity_pt], False)
      ore_pt = ore.get_position()
      if adjacent(entity_pt, ore_pt):
         self.set_resource_count(1 + self.get_resource_count())
         ore.remove_entity(world)
         return ([ore_pt], True)
      else:
         new_pt = world.next_position(entity_pt, ore_pt)
         return (world.move_entity(self, new_pt), False)

   def create_miner_not_full_action(self, world, i_store):
      def action(current_ticks):
         self.remove_pending_action(action)

         entity_pt = self.get_position()
         ore = world.find_nearest(entity_pt, Ore)
         (tiles, found) = self.miner_to_ore(world, ore)

         new_entity = self
         if found:
            new_entity =  self.try_transform_miner(world,
               self.try_transform_miner_not_full)

         new_entity.schedule_action(world,
            new_entity.create_miner_action(world, i_store),
            current_ticks + new_entity.get_rate())
         return tiles
      return action

   def try_transform_miner_not_full(self, world):
      if self.resource_count < self.resource_limit:
         return self
      else:
         new_entity = MinerFull(
            self.get_name(), self.get_resource_limit(),
            self.get_position(), self.get_rate(),
            self.get_images(), self.get_animation_rate())
         return new_entity




class MinerFull (Miner):
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      super(MinerFull, self).__init__ (name, position, imgs, animation_rate, rate,
      resource_limit)
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
      self.resource_limit = resource_limit
      self.resource_count = resource_limit
      self.animation_rate = animation_rate
      self.pending_actions = []

   def miner_to_smith(self, world, smith):
      entity_pt = self.get_position()
      if not smith:
         return ([entity_pt], False)
      smith_pt = smith.get_position()
      if adjacent(entity_pt, smith_pt):
         smith.set_resource_count(smith.get_resource_count() +
            self.get_resource_count())
         self.set_resource_count(0)
         return ([], True)
      else:
         new_pt = world.next_position(entity_pt, smith_pt)
         return (world.move_entity(self, new_pt), False)

   def create_miner_full_action(self, world, i_store):
      def action(current_ticks):
         self.remove_pending_action(action)

         entity_pt = self.get_position()
         smith = world.find_nearest(entity_pt, Blacksmith)
         (tiles, found) = self.miner_to_smith(world, smith)

         new_entity = self
         if found:
            new_entity = self.try_transform_miner(world,
               self.try_transform_miner_full)

         new_entity.schedule_action(world,
            new_entity.create_miner_action(world, i_store),
            current_ticks + new_entity.get_rate())
         return tiles
      return action

   def try_transform_miner_full(self, world):
      new_entity = MinerNotFull(
         self.get_name(), self.get_resource_limit(),
         self.get_position(), self.get_rate(),
         self.get_images(), self.get_animation_rate())

      return new_entity

class Vein (NotAnimated):
   def __init__(self, name, rate, position, imgs, resource_distance=1):
      super(Vein, self).__init__ (name, position, imgs, rate)
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
      self.resource_distance = resource_distance
      self.pending_actions = []

   def get_resource_distance(self):
      return self.resource_distance

   def entity_string(self):
         return ' '.join(['vein', self.name, str(self.position.x),
            str(self.position.y), str(self.rate),
            str(self.resource_distance)])

   def schedule_vein(self, world, ticks, i_store):
      self.schedule_action(world, self.create_vein_action(world, i_store),
         ticks + self.get_rate())

   def create_vein_action(self, world, i_store):
      def action(current_ticks):
         self.remove_pending_action(action)

         open_pt = world.find_open_around(self.get_position(),
            self.get_resource_distance())
         if open_pt:
            ore = world.create_ore(
               "ore - " + self.get_name() + " - " + str(current_ticks),
               open_pt, current_ticks, i_store)
            world.add_entity(ore)
            tiles = [open_pt]
         else:
            tiles = []

         self.schedule_action(world,
         self.create_vein_action(world, i_store),
            current_ticks + self.get_rate())
         return tiles
      return action

class Ore (NotAnimated):
   def __init__(self, name, position, imgs, rate=5000):
      super(Ore, self).__init__ (name, position, imgs, rate)
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0
      self.rate = rate
      self.pending_actions = []

   def entity_string(self):
         return ' '.join(['ore', self.name, str(self.position.x),
            str(self.position.y), str(v.rate)])

   def schedule_ore(self, world, ticks, i_store):
      self.schedule_action(world,
         self.create_ore_transform_action(world, i_store),
         ticks + self.get_rate())

   def create_ore_transform_action(self, world, i_store):
      def action(current_ticks):
         self.remove_pending_action(action)
         blob = world.create_blob(self.get_name() + " -- blob",
            self.get_position(),
            self.get_rate() // BLOB_RATE_SCALE,
            current_ticks, i_store)

         self.remove_entity(world)
         world.add_entity(blob)

         return [blob.get_position()]
      return action

class Blacksmith (PendingAction):
   def __init__(self, name, position, imgs, resource_limit, rate,
      resource_distance=1):
      super(Blacksmith, self).__init__ (name, position, imgs)
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0
      self.resource_limit = resource_limit
      self.resource_count = 0
      self.rate = rate
      self.resource_distance = resource_distance
      self.pending_actions = []

   def get_rate (self):
      return self.rate

   def get_resource_distance(self):
      return self.resource_distance


   def set_resource_count(self, n):
      self.resource_count = n

   def get_resource_count(self):
      return self.resource_count

   def get_resource_limit(self):
      return self.resource_limit


   def get_resource_distance(self):
      return self.resource_distance

   def entity_string(self):
         return ' '.join(['blacksmith', self.name, str(self.position.x),
            str(self.position.y), str(self.resource_limit),
            str(self.rate), str(self.resource_distance)])

class Obstacle (Entity):
   def __init__(self, name, position, imgs):
      super(Obstacle, self).__init__ (name, position, imgs)
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0

class OreBlob (MovingRate):
   def __init__(self, name, position, rate, imgs, animation_rate):
      super(OreBlob, self).__init__ (name, position, imgs, animation_rate, rate)
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
      self.animation_rate = animation_rate
      self.pending_actions = []

   def entity_string(self):
         return ' '.join(['obstacle', self.name, str(self.position.x),
            str(self.position.y)])

   def schedule_blob(self, world, ticks, i_store):
      self.schedule_action(world, self.create_ore_blob_action(world, i_store),
         ticks + self.get_rate())
      self.schedule_animation(world)


   def remove_entity(self, world):
      for action in self.get_pending_actions():
         world.unschedule_action(action)
      self.clear_pending_actions()
      world.remove_entity(self)

   def blob_to_vein(self, world, vein):
      entity_pt = self.get_position()
      if not vein:
         return ([entity_pt], False)
      vein_pt = vein.get_position()
      if adjacent(entity_pt, vein_pt):
         vein.remove_entity(world)
         return ([vein_pt], True)
      else:
         new_pt = world.blob_next_position(entity_pt, vein_pt)
         old_entity = world.get_tile_occupant(new_pt)
         if isinstance(old_entity, Ore):
            old_entity.remove_entity(world)
         return (world.move_entity(self, new_pt), False)

   def create_ore_blob_action(self, world, i_store):
      def action(current_ticks):
         self.remove_pending_action( action)

         entity_pt = self.get_position()
         vein = world.find_nearest(entity_pt, Vein)
         (tiles, found) = self.blob_to_vein(world, vein)

         next_time = current_ticks + self.get_rate()
         if found:
            quake = world.create_quake(tiles[0], current_ticks, i_store)
            world.add_entity(quake)
            next_time = current_ticks + self.get_rate() * 2

         self.schedule_action(world,
            self.create_ore_blob_action(world, i_store),
            next_time)

         return tiles
      return action

class Quake (Moving):
   def __init__(self, name, position, imgs, animation_rate):
      super(Quake, self).__init__ (name, position, imgs, animation_rate)
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0
      self.animation_rate = animation_rate
      self.pending_actions = []

   def schedule_quake(self, world, ticks):
      self.schedule_animation(world, QUAKE_STEPS)
      self.schedule_action(world, self.create_entity_death_action(world),
         ticks + QUAKE_DURATION)

   def remove_entity(self, world):
      for action in self.get_pending_actions():
         world.unschedule_action(action)
      world.clear_pending_actions(self)
      world.remove_entity(self)


   def create_entity_death_action(self, world):
      def action(current_ticks):
         self.remove_pending_action(action)
         pt = self.get_position()
         self.remove_entity(world)
         return [pt]
      return action

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


def get_image(entity):
   return entity.imgs[entity.current_img]




