''' 2D Point

Created for COS30002 AI for Games, Lab,
by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without
permission.

'''
import math

class Point2D(object):

    __slots__ = ('x','y')

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def copy(self):
        return Point2D(self.x, self.y)

    def __str__(self):
        return '(%5.2f,%5.2f)' % (self.x, self.y)

    # operations
    
    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)
        
    def __mul__(self, scalar):
        return Point2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)
        
    def normalize(self):
        length = math.sqrt(self.x ** 2 + self.y ** 2)
        if length != 0:
            self.x /= length
            self.y /= length

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self