import numpy as np
import pygame

class Object2D:
    _instances = []

    def __init__(self,x,y,size,color,control_style):
        self.pos = np.array([x,y])
        self.color = color
        self.size = size
        self.vel = np.zeros(2)
        self.acc = []
        self.current_acc = np.zeros(2) #current acc for drawing
        self.control_style = control_style
        Object2D._instances.append(self)

    def control_IfElse(self,target):    #assuming target is a tuple
        if self.pos[0] < target[0]:
            self.acc.append(np.array([0.25,0]))
        elif self.pos[0] > target[0]:
            self.acc.append(np.array([-0.25,0]))
        if self.pos[1] < target[1]:
            self.acc.append(np.array([0,0.25]))
        elif self.pos[1] > target[1]:
            self.acc.append(np.array([0,-0.25]))

    def control_PD(self,target):
        k_p = 0.005 # proportional gain
        k_d = 0.07 # derivative gain
        e_px = target[0] - self.pos[0] # positional error
        e_py = target[1] - self.pos[1] # positional error
        e_vx = 0 - self.vel[0] # velocity error, saying I want v_f to be == 0
        e_vy = 0 - self.vel[1] # velocity error, saying I want v_f to be == 0
        x_acc = (k_p*e_px) + (k_d*e_vx)
        y_acc = (k_p*e_py) + (k_d*e_vy)
        self.acc.append(np.array([x_acc,y_acc]))

    @classmethod
    def update(cls,target):
        for obj in Object2D._instances:    
            if obj.control_style == "IfElse":
                obj.control_IfElse(target)
            elif obj.control_style == "PD":
                obj.control_PD(target)
            obj.current_acc = sum(obj.acc)
            obj.vel = obj.vel + obj.current_acc
            obj.pos = obj.pos + obj.vel
            obj.acc = []
    
    @classmethod
    def draw(cls,surface):
        for obj in Object2D._instances:    
            pygame.draw.circle(surface,(255,255,255),tuple(obj.pos),obj.size)
            pygame.draw.circle(surface,obj.color,tuple(obj.pos),obj.size,5)
            # pygame.draw.line(surface,(0,255,0),tuple(obj.pos),tuple(obj.pos + 100*obj.current_acc),3)