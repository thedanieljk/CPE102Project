import point
import actions
import worldmodel

class WorldObject(object):
   def __init__(self,name,imgs):
      self.name = name
      self.imgs = imgs
      self.current_img = 0
   def get_images(self):
      return self.imgs
   def get_name(self):
      return self.name

class WorldEntity(WorldObject):
   def __init__(self,name,imgs,position):
      self.position = position
      super(WorldEntity,self).__init__(name,imgs)
   def set_position(self,point):
      self.position = point
   def get_position(self):
      return self.position

class Actor(WorldEntity):
   def __init__(self,name,imgs,position):
      super(Actor,self).__init__(name,imgs,position)
      self.pending_actions = []
   def remove_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.remove(action)
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

class AnimatedActor(Actor):
   def __init__(self,name,imgs,position,animation_rate):
      super(AnimatedActor,self).__init__(name,imgs,position)
      self.animation_rate = animation_rate
   def get_animation_rate(self):
      return self.animation_rate

class Mover(AnimatedActor):
   def __init__(self,name,imgs,position,animation_rate,rate):
      super(Mover,self).__init__(name,imgs,position,animation_rate)
      self.rate = rate
   def get_rate(self):
      return self.rate

class Miner(Mover):
   def __init__(self,name,imgs,position,animation_rate,rate,resource_limit):
      super(Miner,self).__init__(name,imgs,position,animation_rate,rate)
      self.resource_limit = resource_limit
      self.resource_count = 0
   def set_resource_count(self, n):
      self.resource_count = n
   def get_resource_count(self):
      return self.resource_count
   def get_resource_limit(self):
      return self.resource_limit
 
class Background(WorldObject):
   def __init__(self, name, imgs):
      super(Background,self).__init__(name,imgs)


class MinerNotFull(Miner):
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      super(MinerNotFull,self).__init__(name,imgs,position,animation_rate,rate,resource_limit)
   def entity_string(self):                                                       
      return ' '.join(['miner', self.name, str(self.position.x),
          str(self.position.y), str(self.resource_limit),
          str(self.rate), str(self.animation_rate)])
   def miner_to_ore(self,world, ore):
      entity_pt = self.get_position()
      if not ore:
         return ([entity_pt], False)
      ore_pt = ore.get_position()
      if actions.adjacent(entity_pt, ore_pt):
         self.set_resource_count(
             1 + self.get_resource_count())
         worldmodel.remove_entity(world, ore)
         return ([ore_pt], True)
      else:
         new_pt = actions.next_position(world, entity_pt, ore_pt)
         return (worldmodel.move_entity(world, self, new_pt), False)

class MinerFull(Miner):
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      self.resource_count = resource_limit
      super(MinerFull,self).__init__(name,imgs,position,animation_rate,rate,resource_limit)
   def miner_to_smith(self,world, smith):
      entity_pt = self.get_position()
      if not smith:
         return ([entity_pt], False)
      smith_pt = smith.get_position()
      if actions.adjacent(entity_pt, smith_pt):
         smith.set_resource_count(
            smith.get_resource_count() +
            self.get_resource_count())
         self.set_resource_count(0)
         return ([], True)
      else:
         new_pt = actions.next_position(world, entity_pt, smith_pt)           
         return (worldmodel.move_entity(world, self, new_pt), False)

class Vein(Actor):
   def __init__(self, name, rate, position, imgs, resource_distance=1):
      self.resource_distance = resource_distance
      self.rate = rate
      super(Vein,self).__init__(name,imgs,position)
   def get_rate(self):
      return self.rate
   def get_resource_distance(self):
      return self.resource_distance
   def entity_string(self):                                                     
       return ' '.join(['vein', self.name, str(self.position.x),
          str(self.position.y), str(self.rate),
          str(self.resource_distance)])

class Ore(Actor):
   def __init__(self, name, position, imgs, rate=5000):
      self.rate = rate
      super(Ore,self).__init__(name,imgs,position)
   def get_rate(self):
      return self.rate
   def entity_string(self):                                                         
      return ' '.join(['ore', self.name, str(self.position.x),
          str(self.position.y), str(self.rate)])

class Blacksmith(WorldEntity):
   def __init__(self, name, position, imgs, resource_limit, rate,
      resource_distance=1):
      super(Blacksmith,self).__init__(name,imgs,position)
      self.rate = rate
      self.resource_limit = resource_limit
      self.resource_count = 0
      self.resource_distance = resource_distance
   def get_rate(self):
      return self.rate 
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

class Obstacle(WorldEntity):
   def __init__(self, name, position, imgs):
      super(Obstacle,self).__init__(name,imgs,position)
   def entity_string(self):                                           
      return ' '.join(['obstacle', self.name, str(self.position.x),
          str(self.position.y)])

class OreBlob(Mover):
   def __init__(self, name, position, rate, imgs, animation_rate):
      super(OreBlob,self).__init__(name,imgs,position,animation_rate,rate)

class Quake(AnimatedActor):
   def __init__(self, name, position, imgs, animation_rate):
      super(Quake,self).__init__(name,imgs,position,animation_rate)
   def get_animation_rate(self):
      return self.animation_rate

def get_image(entity):
   return entity.imgs[entity.current_img]
def next_image(entity):
   entity.current_img = (entity.current_img + 1) % len(entity.imgs)




