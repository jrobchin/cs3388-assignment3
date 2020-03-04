from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricPlane(parametricObject):

    def __init__(self,T=matrix(np.identity(4)),width=1.0,height=1.0,color=(0,0,0),reflectance=(0.0,0.0,0.0,0.0),uRange=(0.0,0.0),vRange=(0.0,0.0),uvDelta=(0.0,0.0)):
        super().__init__(T,color,reflectance,uRange,vRange,uvDelta)
        self.__width = width
        self.__height = height

    def getPoint(self,u,v):
        P = matrix(np.ones((4,1)))
        P.set(0,0,u*self.__width)
        P.set(1,0,v*self.__height)
        P.set(2,0,0.0)
        return P

    def setHeight(self,height):
        self.__height = height

    def getHeight(self):
        return self.__height

    def setWidth(self,width):
        self.__width = width

    def getWidth(self):
        return self.__width