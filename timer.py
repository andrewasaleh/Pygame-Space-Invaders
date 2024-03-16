class Timer: 
  def __init__(self, image_list, start_index=0, delta=6, looponce=False): 
    self.image_list = image_list
    self.delta = delta
    self.looponce = looponce
    self.index = start_index
    self.time = 0

  def update_index(self):
    self.time += 1
    if self.time >= self.delta:
      self.index += 1
      self.time = 0
      if self.index > len(self.image_list) - 1 and not self.finished():
        self.index = 0

  def finished(self): 
    finished = self.looponce and self.index >= len(self.image_list) - 1
    return finished
  
  def current_index(self): return self.index

  def current_image(self):     # self.time = 0
    self.update_index()
    return self.image_list[self.index]
  
  