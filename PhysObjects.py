import numpy as np
import pygame

class Object2D:
    """
    Object with automated 2D (x & y) control logic.
    """
    _instances = [] # Stores the instances of the class for class-methods

    def __init__(self,x,y,size,color,control_style):
        """
        Initializes the object with position, size and color (for drawing), and control style

        Args:
            x,y (float):    Used to form the position numpy vector (could also be pygame.math.Vector2)
            size (int):     Size used for drawing the object
            color (tuple):  RGB tuple
            control_style (string): String used to determine what control loop to utilize ('IfElse' or 'PD')
        Inits:
            self.pos (numpy 2D vector): Position
            self.color, self.size:  Drawing parameters
            self.vel (numpy 2D vector): Object velocity, initialized as a zero-vector
            self.acc (list):    Empty list used to store all accelerations acting on the object (for this code as it currently is, this method is unecessary and it could simply be a vector)
            self.current_acc (numpy 2D vector): The resulting acceleration vector from summing up all of the accelerations in self.acc (again, this is overkill for this current code)
            self.control_style (string):    Used later to determine what control loop to use
            Appends the object to the list of class instances
        """
        self.pos = np.array([x,y])
        self.color = color
        self.size = size
        self.vel = np.zeros(2)
        self.acc = []
        self.current_acc = np.zeros(2) #current acc for drawing
        self.control_style = control_style
        Object2D._instances.append(self)

    def control_IfElse(self,target):    #assuming target is a tuple
        """
        Simple control loop. Says to constantly accelerate the object towards the target.
        Args:
            target (tuple): Position of the target 
        Returns:
            Appends the accelerations to self.acc, which is summed up later in the update() method
        """
        if self.pos[0] < target[0]: # X-component acceleration
            self.acc.append(np.array([0.25,0]))
        elif self.pos[0] > target[0]:
            self.acc.append(np.array([-0.25,0]))
        if self.pos[1] < target[1]: # Y-component acceleration
            self.acc.append(np.array([0,0.25]))
        elif self.pos[1] > target[1]:
            self.acc.append(np.array([0,-0.25]))

    def control_PD(self,target):
        """
        Proportional-derivative control loop. Its goal is to approach and come to rest at the target position.
        The object's velocity will almost never be 0, as it will oscillate around the target by some miniscule distance.
        In order to achieve true 0-velocity, recommend using a proprotional-integral-derivative (PID) control loop,
        which this code does not currently have.
        Args:
            target (tuple): Position of the target
        Returns:
            Appends the x and y-component accelerations to self.acc
        """
        k_p = 0.005 # proportional gain
        k_d = 0.07 # derivative gain
        e_px = target[0] - self.pos[0] # positional error
        e_py = target[1] - self.pos[1] # positional error
        e_vx = 0 - self.vel[0] # velocity error, saying I want v_f to be == 0
        e_vy = 0 - self.vel[1] # velocity error, saying I want v_f to be == 0
        x_acc = (k_p*e_px) + (k_d*e_vx) # Fundamental PD control-loop formula
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