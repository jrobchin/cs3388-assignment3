from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricCircle(parametricObject):

    def __init__(self,T=matrix(np.identity(4)),radius=1.0,color=(0,0,0),reflectance=(0.0,0.0,0.0,0.0),uRange=(0.0,0.0),vRange=(0.0,0.0),uvDelta=(0.0,0.0)):
        super().__init__(T,color,reflectance,uRange,vRange,uvDelta)
        self.__radius = radius

    def getPoint(self,u,v):
        P = matrix(np.ones((4,1)))
        P.set(0,0,u*self.__radius*cos(v))
        P.set(1,0,u*self.__radius*sin(v))
        P.set(2,0,0.0)
        return P

    def setHeight(self,height):
        self.__height = height

    def getHeight(self):
        return self.__height

    def setRadius(self,radius):
        self.__radius = radius

    def getRadius(self):
        return self.__radius