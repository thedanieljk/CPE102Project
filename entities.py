#I honestly just couldn't figure out
#the syntax in time. I spent so much
#time working on this but I couldn't
#figure it out by myself without
#spending a ton of time

import point

class Background:
   def __init__(self, name, imgs):
      self.name = name
      self.imgs = imgs
      self.current_img = 0
   def get_images(self):
      return self.imgs

class Entity(object):
   def __init__(self,name,position,rate,imgs):
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
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
class MinerNotFull(Entity):
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      self.resource_limit = resource_limit
      self.resource_count = 0
      self.animation_rate = animation_rate
      self.pending_actions = []
      super(MinerNotFull,self).__init__(name,position,rate,imgs)
   def set_resource_count(self, n):
      self.resource_count = n
   def get_resource_count(self):
      return self.resource_count
   def get_resource_limit(self):
      return self.resource_limit
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
   def entity_string(self):                                                       
      return ' '.join(['miner', self.name, str(self.position.x),
          str(self.position.y), str(self.resource_limit),
          str(self.rate), str(self.animation_rate)])
class MinerFull(Entity):
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      self.resource_limit = resource_limit
      self.resource_count = resource_limit
      self.animation_rate = animation_rate
      self.pending_actions = []
      super(MinerFull,self).__init__(name,position,rate,imgs)
   def set_resource_count(self, n):
      self.resource_count = n
   def get_resource_count(self):
      return self.resource_count
   def get_resource_limit(self):
      return self.resource_limit
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
class Vein(Entity):
   def __init__(self, name, rate, position, imgs, resource_distance=1):
      self.resource_distance = resource_distance
      self.pending_actions = []
      super(Vein,self).__init__(name,position,rate,imgs)
   def get_resource_distance(self):
      return self.resource_distance
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
   def entity_string(self):                                                     
       return ' '.join(['vein', self.name, str(self.position.x),
          str(self.position.y), str(self.rate),
          str(self.resource_distance)])
class Ore(Entity):
   def __init__(self, name, position, imgs, rate=5000):
      self.pending_actions = []
      super(Ore,self).__init__(name,position,rate,imgs)
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
   def entity_string(self):                                                         
      return ' '.join(['ore', self.name, str(self.position.x),
          str(self.position.y), str(self.rate)])
class Blacksmith(Entity):
   def __init__(self, name, position, imgs, resource_limit, rate,
      resource_distance=1):
      self.resource_limit = resource_limit
      self.resource_count = 0
      self.resource_distance = resource_distance
      self.pending_actions = []
      super(Blacksmith,self).__init__(name,position,rate,imgs)
   def set_resource_count(self, n):
      self.resource_count = n
   def get_resource_count(self):
      return self.resource_count
   def get_resource_limit(self):
      return self.resource_limit
   def get_resource_distance(self):
      return self.resource_distance
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
   def entity_string(self):                                                       
       return ' '.join(['blacksmith', self.name, str(self.position.x),
          str(self.position.y), str(self.resource_limit),
          str(self.rate), str(self.resource_distance)])
class Obstacle:
   def __init__(self, name, position, imgs):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0
   def set_position(self, point):
      self.position = point
   def get_position(self):
      return self.position
   def get_images(self):
      return self.imgs
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
   def get_name(self):
      return self.name
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
   def entity_string(self):                                           
      return ' '.join(['obstacle', self.name, str(self.position.x),
          str(self.position.y)])
class OreBlob(Entity):
   def __init__(self, name, position, rate, imgs, animation_rate):
      self.animation_rate = animation_rate
      self.pending_actions = []
      super(OreBlob,self).__init__(name,position,rate,imgs)
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
class Quake:
   def __init__(self, name, position, imgs, animation_rate):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0
      self.animation_rate = animation_rate
      self.pending_actions = []
   def set_position(self, point):
      self.position = point
   def get_position(self):
      return self.position
   def get_images(self):
      return self.imgs
   def get_rate(self):
      return self.rate
   def set_resource_count(self, n):
      self.resource_count = n
   def get_resource_limit(self):
      return self.resource_limit
   def get_resource_distance(self):
      return self.resource_distance
   def get_name(self):
      return self.name
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




