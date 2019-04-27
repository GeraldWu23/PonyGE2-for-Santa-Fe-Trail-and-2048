#------------------- read file -------------------------
import numpy as np
from copy import deepcopy

with open('D:/PythonCode/PonyGE2-master/src/santa_fe_trail.txt') as f:
    santa_fe_trail_graph = []
    for line in f.readlines():      
        santa_fe_trail_graph.append(line[:32])

santa_fe_trail = np.zeros((32,32))
for y in range(32):
    for x in range(32):
        if santa_fe_trail_graph[y][x] == 'x':
            santa_fe_trail[y][x] = 1


#------------------- ant class -------------------------


'''

   UP    = ( 0,-1)
   DOWN  = ( 0, 1)
   LEFT  = (-1, 0)
   RIGHT = ( 1, 0)

'''


class Ant:
    def __init__(self):
        self.position  = np.array([0,0])
        self.direction = 0
        self.food      = 1  # the food that has had
        self.graph     = deepcopy(santa_fe_trail)   
        self.graph[0][0] = 0  # already had the first food
        self.count     = 0

    def get_next(self):
        direction = self.direction
        return np.array([int(np.cos(direction * np.pi/2)) ,int(np.sin(direction * np.pi/2))])


    def turn_left(self):
        self.direction -= 1
        self.count     += 1
        
    def turn_right(self):
        self.direction += 1
        self.count     += 1
    
    def move(self):
        next_step = self.get_next()
        next_place = self.position + next_step
        
        next_place[0] %= 32
        next_place[1] %= 32
        
        if next_place[0] >= 0 and next_place[1] >= 0 and next_place[0] < 32 and next_place[1] < 32:
            self.position = next_place
            self.count   += 1  # if not out of bound, count a movement

            
        x,y = self.position
        if self.graph[y][x] == 1: # if there is food in new position, eat it
            self.food += 1
            self.graph[y][x] = 0  
            
        return self.position
    
    
    def food_ahead(self):
        next_step = self.get_next()
        next_place = self.position + next_step
        
        x,y = next_place
        if self.graph[y % 32][x % 32] == 1:
            return True
        
        return False


#------------------ testing ------------------------