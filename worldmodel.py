import entities
import pygame
import ordered_list
import actions
import occ_grid
import point

class WorldModel:
   def __init__(self, num_rows, num_cols, background):
      self.background = occ_grid.Grid(num_cols, num_rows, background)
      self.num_rows = num_rows
      self.num_cols = num_cols
      self.occupancy = occ_grid.Grid(num_cols, num_rows, None)
      self.entities = []
      self.action_queue = ordered_list.OrderedList()
   def add_pending_action(self, action):
      if hasattr(self, "pending_actions"):
          self.pending_actions.append(action) 
   def get_pending_actions(self):
      if hasattr(self, "pending_actions"):
          return self.pending_actions
      else:
          return [] 
   def clear_pending_actions(self):
      if hasattr(self, "pending_actions"):
          self.pending_actions = []
   def within_bounds(self, pt):
      return (pt.x >= 0 and pt.x < self.num_cols and
          pt.y >= 0 and pt.y < self.num_rows)
   def is_occupied(self, pt):
      return (self.within_bounds(pt) and
          occ_grid.get_cell(self.occupancy, pt) != None)
   def schedule_action(self,action, time):
     self.action_queue.insert(action, time)
   def unschedule_action(self,action):
     self.action_queue.remove(action)
   def update_on_time(world, ticks):
     tiles = []
 
     next = world.action_queue.head()
     while next and next.ord < ticks:
         world.action_queue.pop()
         tiles.extend(next.item(ticks))  # invoke action function
         next = world.action_queue.head()
     return tiles
   def get_background_image(self,pt):
     if self.within_bounds(pt):
         return entities.get_image(occ_grid.get_cell(self.background, pt))
   def get_background(self, pt):
     if within_bounds(self, pt):
         return occ_grid.get_cell(self.background, pt)
   def set_background(self, pt, bgnd):
     if self.within_bounds(pt):
         occ_grid.set_cell(self.background, pt, bgnd)
   def get_tile_occupant(self, pt):
     if self.within_bounds(pt):
         return occ_grid.get_cell(self.occupancy, pt) 
   def get_entities(self):
     return self.entities 


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


def find_nearest(world, pt, type):
   oftype = [(e, distance_sq(pt, e.get_position()))
      for e in world.entities if isinstance(e, type)]

   return nearest_entity(oftype)


def add_entity(world, entity):
   pt = entity.get_position()
   if world.within_bounds(pt):
      old_entity = occ_grid.get_cell(world.occupancy, pt)
      if old_entity != None:
         old_entity.clear_pending_actions()
      occ_grid.set_cell(world.occupancy, pt, entity)
      world.entities.append(entity)


def move_entity(world, entity, pt):
   tiles = []
   if world.within_bounds(pt):
      old_pt = entity.get_position()
      occ_grid.set_cell(world.occupancy, old_pt, None)
      tiles.append(old_pt)
      occ_grid.set_cell(world.occupancy, pt, entity)
      tiles.append(pt)
      entity.set_position(pt)

   return tiles


def remove_entity(world, entity):
   remove_entity_at(world, entity.get_position())


def remove_entity_at(world, pt):
   if (world.within_bounds(pt) and
      occ_grid.get_cell(world.occupancy, pt) != None):
      entity = occ_grid.get_cell(world.occupancy, pt)
      entity.set_position(point.Point(-1, -1))
      world.entities.remove(entity)
      occ_grid.set_cell(world.occupancy, pt, None)





