import point
import actions
import worldmodel
#did not include entity_string in a parent class
#felt that it would have to be redefined
#too many times to be worth it

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
   def __init__(self,name,imgs,position,rate):
      super(Actor,self).__init__(name,imgs,position)
      self.rate = rate
   def get_rate(self):
      return self.rate
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

class Background(WorldObject): #has such little input, not worth using inheritance
   def __init__(self, name, imgs):
      super(Background,self).__init__(name,imgs)

class Entity(object): #main parent class
   def __init__(self,name,position,rate,imgs):
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
      self.pending_actions = []
   def set_position(self,point):
      self.position = point
   def get_position(self):
      return self.position
   def get_images(self):
      return self.imgs
   def get_rate(self):
      return self.rate
   def get_name(self):
      return self.name
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

class OtherEnt(object): #second parent class for irregular entities
   def __init__(self,name,position,imgs):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0
   def set_position(self,point):
      self.position = point
   def get_position(self):
      return self.position
   def get_images(self):
      return self.imgs
 
class Miner(Entity): #simplification of miner related classes using sub-inheritance. Entity -> Miner -> Miner related
   def __init__(self,name,position,rate,imgs,resource_limit,animation_rate):
      self.resource_limit = resource_limit
      self.resource_count = 0
      self.animation_rate = animation_rate
      super(Miner,self).__init__(name,position,rate,imgs)
   def set_resource_count(self, n):
      self.resource_count = n
   def get_resource_count(self):
      return self.resource_count
   def get_resource_limit(self):
      return self.resource_limit
   def get_animation_rate(self):
      return self.animation_rate

class MinerNotFull(Miner): #inherits from Miner! Entity -> Miner -> MinerNotFull
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      super(MinerNotFull,self).__init__(name,position,rate,imgs,resource_limit,animation_rate)
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

class MinerFull(Miner): #inherits from Miner! Entity -> Miner -> MinerNotFull
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      self.resource_count = resource_limit
      super(MinerFull,self).__init__(name,position,rate,imgs,resource_limit,animation_rate)
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
      super(Vein,self).__init__(name,imgs,position,rate)
   def get_resource_distance(self):
      return self.resource_distance
   def entity_string(self):                                                     
       return ' '.join(['vein', self.name, str(self.position.x),
          str(self.position.y), str(self.rate),
          str(self.resource_distance)])

class Ore(Actor):
   def __init__(self, name, position, imgs, rate=5000):
      super(Ore,self).__init__(name,imgs,position,rate)
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

class OreBlob(Entity):
   def __init__(self, name, position, rate, imgs, animation_rate):
      self.animation_rate = animation_rate
      super(OreBlob,self).__init__(name,position,rate,imgs)
   def get_animation_rate(self):
      return self.animation_rate

class Quake(OtherEnt):
   def __init__(self, name, position, imgs, animation_rate):
      self.animation_rate = animation_rate
      self.pending_actions = []
      super(Quake,self).__init__(name,position,imgs)
   def get_animation_rate(self):
      return self.animation_rate
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

def get_image(entity):
   return entity.imgs[entity.current_img]
def next_image(entity):
   entity.current_img = (entity.current_img + 1) % len(entity.imgs)




