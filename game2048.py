# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 20:02:05 2018

@author: wukak
"""
from copy import deepcopy,copy
import numpy as np
OUTOFBOUND = 16
OUTOFBOUNDVAL = 16000

class game2048:
    class _Node:
        def __init__(self,row,col):
            self.value = 0
            self.position = row*4+col
            self.merge_in_this_turn = False #did this node experience a merging in this turn
            self.row = row
            self.col = col
            self.left_place = self.row*4
            self.right_place = 4*self.row + 3
            self.up_place = self.col
            self.down_place = 12 + self.col
            
        
        
    def __init__(self):
        self.biggestvalue = 2
        self.grids = []
        for row in range(4):
            for col in range(4):
                self.grids += [self._Node(row,col)]
        self.grids += [self._Node(4,0)] #OUTOFBOUND
        self.grids[-1].value = OUTOFBOUNDVAL #outofbound value
        self.oldstate = self.grids
        self.area = 0  # the space with number
        self.move_count = 0
        
        
    def findNear(self,node,direction):
        left_place = node.left_place
        right_place = node.right_place
        up_place = node.up_place
        down_place = node.down_place
        grids_place = node.position
        
        if direction == 'left':
            if grids_place == left_place:
                return self.grids[16] #if it's already the bound, the near will be outofbound
            near = self.grids[grids_place-1]
            if near.value == 0:
                near = self.findNear(near,'left')
                
        elif direction == 'right':
            if grids_place == right_place:
                return self.grids[16]
            near = self.grids[grids_place+1] #if it's already the bound, the near will be outofbound
            if near.value == 0:
                near = self.findNear(near,'right')
                
        elif direction == 'up':
            if grids_place == up_place:
                return self.grids[16] #if it's already the bound, the near will be outofbound
            near = self.grids[max(up_place,grids_place-4)]
            if near.value == 0:
                near = self.findNear(near,'up')
                
        else:
            if grids_place == down_place:
                return self.grids[16] #if it's already the bound, the near will be outofbound
            near = self.grids[min(down_place,grids_place+4)]
            if near.value == 0:
                near = self.findNear(near,'down')
                
        return near
    
    
    def findNearBlank(self,node,direction):
        left_place = node.left_place
        right_place = node.right_place
        up_place = node.up_place
        down_place = node.down_place
        
        if direction == 'left':
            near = self.findNear(node,'left')
            if near == self.grids[OUTOFBOUND]: #if near is out of bound
                return self.grids[left_place]  
            else:
                return self.grids[near.position+1] #right grid of near
        elif direction == 'right':
            near = self.findNear(node,'right')
            if near == self.grids[OUTOFBOUND]: #if near is out of bound
                return self.grids[right_place]
            else:
                return self.grids[near.position-1] #left grid of near
        elif direction == 'up':
            near = self.findNear(node,'up')
            if near == self.grids[OUTOFBOUND]: #if near is out of bound
                return self.grids[up_place]
            else:
                return self.grids[near.position+4] #down grid of near
                
        else:
            near = self.findNear(node,'down')
            if near == self.grids[OUTOFBOUND]: #if out of bound
                return self.grids[down_place]
            else:
                return self.grids[near.position-4] #up grid of near
    
    
    def merge(self,node_move,node_still): #node_move moves its value to node_still
        if node_move.value != node_still.value:
            print("CAN'T MERGE BECAUSE OF DIFFERENT VALUES")
            return False
        if node_still.merge_in_this_turn == True: #double check if it's merged in this term
            return True
        node_move.value = 0
        node_still.value *= 2
        node_still.merge_in_this_turn = True
        return True
    
    
    def findZeros(self):
        zeros_loc = []
        for grid in range(16):
            if self.grids[grid].value == 0:
                zeros_loc += [grid]
        zeros_loc = sorted(zeros_loc)
        return zeros_loc
    
    
    def generateNode(self):
        empty_num = 0
        for grid in range(16):
            if self.grids[grid].value == 0:
                empty_num += 1
        if empty_num>0:
            generateIn = np.random.randint(empty_num)
            countempty = 0
            generateNum = 2*np.random.randint(1,3) # choose a number in (2,4) to fill in
            for i in range(16):
                if self.grids[i].value == 0:
                    if countempty == generateIn:
                        self.grids[i].value = generateNum
                        break
                    countempty += 1
    
    
    def show(self):
        for i in range(4):
            print([self.grids[i*4+j].value for j in range(4)])
        print()
        print()
    
    
    def move_left(self):
        for row in range(4):
            for col in range(4): #from left to right
                position = row*4+col
                node = self.grids[position]
                near = self.findNear(node,'left')
                near_blank = self.findNearBlank(node,'left')
                if near.value == OUTOFBOUNDVAL: #there is no node on the left
                    value = node.value
                    node.value = 0
                    self.grids[node.left_place].value = value
                elif near.value != node.value or near.merge_in_this_turn == True: #have different value with near or it has been merged
                    value = node.value
                    node.value = 0
                    near_blank.value = value
                    
                elif near.value == node.value: #have the same value with near
                    self.merge(node,near)
        
        self.checkend() #check if it ends
        zeros_loc = range(16)
        if zeros_loc != self.findZeros():
            self.generateNode()
            zeros_loc = self.findZeros()
                
        area = self.check_area()
#        print('area: '+str(area)+str(self.area))  
#        self.show()
        
        for grid in self.grids: #refresh merge statuses
            grid.merge_in_this_turn = False
            
        self.move_count += 1
        self.get_biggest()
        
        return area
                
                
                    
    def move_right(self):
        for row in range(4):
            for col in range(4)[::-1]: #from right to left
                position = row*4+col
                node = self.grids[position]
                near = self.findNear(node,'right')
                near_blank = self.findNearBlank(node,'right')
                if near.value == OUTOFBOUNDVAL: #there is no node on the right
                    value = node.value
                    node.value = 0
                    self.grids[node.right_place].value = value
                elif near.value != node.value or near.merge_in_this_turn == True: #have different value with near or it has been mergedr
                    value = node.value
                    node.value = 0
                    near_blank.value = value
                elif near.value == node.value: #have the same value with near
                    self.merge(node,near)
            
        self.checkend() #check if it ends
        zeros_loc = range(16)
        if zeros_loc != self.findZeros():
            self.generateNode()
            zeros_loc = self.findZeros()
                
        area = self.check_area()
#        print('area: '+str(area)+str(self.area))  
#        self.show()
        
        for grid in self.grids: #refresh merge statuses
            grid.merge_in_this_turn = False
        
        self.move_count += 1
        self.get_biggest()
        
        return area
        
                    
                    
    def move_up(self):
        for row in range(4): #from up to down
            for col in range(4):
                position = row*4+col 
                 
                node = self.grids[position]
                near = self.findNear(node,'up')
                near_blank = self.findNearBlank(node,'up')
                if near.value == OUTOFBOUNDVAL: #there is no node on the top
                    value = node.value
                    node.value = 0
                    self.grids[node.up_place].value = value
                elif near.value != node.value or near.merge_in_this_turn == True: #have different value with near or it has been merged
                    value = node.value
                    node.value = 0
                    near_blank.value = value
                elif near.value == node.value: #have the same value with near
                    self.merge(node,near)
        
        self.checkend() #check if it ends
        zeros_loc = range(16)
        if zeros_loc != self.findZeros():
            self.generateNode()
            zeros_loc = self.findZeros()
                
        area = self.check_area()
#        print('area: '+str(area)+str(self.area))  
#        self.show()
        
        for grid in self.grids: #refresh merge statuses
            grid.merge_in_this_turn = False
        
        self.move_count += 1
        self.get_biggest()
        
        return area
        

            
    def move_down(self):
        for row in range(4)[::-1]:
            for col in range(4):
                position = row*4+col
                node = self.grids[position]
                near = self.findNear(node,'down')
                near_blank = self.findNearBlank(node,'down')
                if near.value == OUTOFBOUNDVAL: #there is no node on the bottom
                    value = node.value
                    node.value = 0
                    self.grids[node.down_place].value = value
                elif near.value != node.value or near.merge_in_this_turn == True: #have different value with near or it has been merged
                    value = node.value
                    node.value = 0
                    near_blank.value = value
                elif near.value == node.value: #have the same value with near
                    self.merge(node,near)
            
        self.checkend() #check if it ends
        zeros_loc = range(16)
        if zeros_loc != self.findZeros():
            self.generateNode()
            zeros_loc = self.findZeros()
        
        area = self.check_area()
#        print('area: '+str(area)+str(self.area))  
#        self.show()
        
        for grid in self.grids: #refresh merge statuses
            grid.merge_in_this_turn = False
        
        self.move_count += 1
        self.get_biggest()
        
        return area
    
    
    def checkend(self): #check if the game ends
        
        #Win
        maxnum = 0
        for grid in range(16):
            if self.grids[grid].value > maxnum:
                maxnum = self.grids[grid].value
        if maxnum == 512:
#            self.show()
#            print
#            print
#            print('***********************')
#            print('*******         *******')
#            print('******* You Win *******')
#            print('*******         *******')
#            print('***********************') 
            return True
        
        #Lose
        for grid in self.grids: ########################### if you dont move well when it's full it's still lose
            if grid.value == 0: #check before generating, if no place for generating, lose
                return False
#        print
#        print
#        print('************************')
#        print('*******          *******')
#        print('******* Full Grid ******')
#        print('*******          *******')
#        print('************************')
        return True
    
    
    def get_biggest(self):
        tmp = 0
        for i in range(16):
            grid = self.grids[i].value
            if tmp < grid:
                tmp = grid
        self.biggestvalue = copy(tmp)
        return self.biggestvalue
        
    
    def check_area(self):  # check if the area is smaller
        tmp = copy(self.area)
        count = 0
        for i in range(16):
            grid = self.grids[i]
            if grid.value != 0:
                count += 1
        
        if count <= tmp:
            self.area = copy(count)
#            print(self.area)
            return True
        else:
            self.area = copy(count)
#            print(self.area)
            return False


    def look_up(self):
        old_area = copy(self.area)
        self.oldstate = deepcopy(self.grids)
        result = self.move_up()
        self.grids = deepcopy(self.oldstate)
        self.area = copy(old_area)
        return result
    
    
    def look_down(self):
        old_area = copy(self.area)
        self.oldstate = deepcopy(self.grids)
        result = self.move_down()
        self.grids = deepcopy(self.oldstate)
        self.area = copy(old_area)
        return result
    
    
    def look_left(self):
        old_area = copy(self.area)
        self.oldstate = deepcopy(self.grids)
        result = self.move_left()
        self.grids = deepcopy(self.oldstate)
        self.area = copy(old_area)
        return result
    
    
    def look_right(self):
        old_area = copy(self.area)
        self.oldstate = deepcopy(self.grids)
        result = self.move_right()
        self.grids = deepcopy(self.oldstate)
        self.area = copy(old_area)
        return result
    
    
    
    def run(self):
        self.generateNode()
        while(1):
                
            inp = input('w for up, s for down, a for left, d for right')

            if inp == 'w':
                self.move_up()
            elif inp == 's':      
                self.move_down()
            elif inp == 'a':
                self.move_left()
            elif inp == 'd':
                self.move_right()          
            elif inp == 'q':
                break
            elif inp == 'i':
                print(self.look_up())
            elif inp == 'k':
                print(self.look_down())
            elif inp == 'j':
                print(self.look_left())
            elif inp == 'l':
                print(self.look_right())
            print(self.get_biggest())

    
    def cmd_run(self):
        self.generateNode()
        
#        while(1):
#            inp = input('w for up, s for down, a for left, d for right')
#
#            if inp == 'w':
#                self.move_up()
#            elif inp == 's':      
#                self.move_down()
#            elif inp == 'a':
#                self.move_left()
#            elif inp == 'd':
#                self.move_right()          
#            elif inp == 'q':
#                break
            









