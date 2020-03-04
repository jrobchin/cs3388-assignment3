from math import *
import numpy as np
from matrix import matrix

class cameraMatrix:

    def __init__(self,UP,E,G,nearPlane=10.0,farPlane=50.0,width=640,height=480,theta=90.0):
        self.__np = nearPlane
        self.__fp = farPlane
        Mp = self.__setMp(nearPlane,farPlane)
        T1 = self.__setT1(nearPlane,theta,width/height)
        S1 = self.__setS1(nearPlane,theta,width/height)
        T2 = self.__setT2()
        S2 = self.__setS2(width,height)
        W2 = self.__setW2(height)

        self.__UP = UP.normalize()
        self.__N = (E - G).removeRow(3).normalize()
        self.__U = self.__UP.removeRow(3).transpose().crossProduct(self.__N.transpose()).normalize().transpose()
        self.__V = self.__N.transpose().crossProduct(self.__U.transpose()).transpose()
        self.__Mv = self.__setMv(self.__U,self.__V,self.__N,E)
        self.__C = W2*S2*T2*S1*T1*Mp
        self.__M = self.__C*self.__Mv

    def __setMv(self,U,V,N,E):
        Mv = matrix(np.identity(4))
        Mv.set(0,0,U.get(0,0))
        Mv.set(0,1,U.get(1,0))
        Mv.set(0,2,U.get(2,0))
        Mv.set(0,3,(-E.removeRow(3).transpose()*U).get(0,0))

        Mv.set(1,0,V.get(0,0))
        Mv.set(1,1,V.get(1,0))
        Mv.set(1,2,V.get(2,0))
        Mv.set(1,3,(-E.removeRow(3).transpose()*V).get(0,0))

        Mv.set(2,0,N.get(0,0))
        Mv.set(2,1,N.get(1,0))
        Mv.set(2,2,N.get(2,0))
        Mv.set(2,3,(-E.removeRow(3).transpose()*N).get(0,0))
        return Mv

    def __setMp(self,nearPlane,farPlane):
        Mp = matrix(np.identity(4))
        Mp.set(0,0,nearPlane)
        Mp.set(1,1,nearPlane)
        Mp.set(2,2,-(farPlane+nearPlane)/(farPlane-nearPlane))
        Mp.set(2,3,-2.0*(farPlane*nearPlane)/(farPlane-nearPlane))
        Mp.set(3,2,-1.0)
        Mp.set(3,3,0.0)
        return Mp

    def __setT1(self,nearPlane,theta,aspect):
        top = nearPlane*tan(pi/180.0*theta/2.0)
        right = aspect*top
        bottom = -top
        left = -right
        T1 = matrix(np.identity(4))
        T1.set(0,3,-(right+left)/2.0)
        T1.set(1,3,-(top+bottom)/2.0)
        return T1

    def __setS1(self,nearPlane,theta,aspect):
        top = nearPlane*tan(pi/180.0*theta/2.0)
        right = aspect*top
        bottom = -top
        left = -right
        S1 = matrix(np.identity(4))
        S1.set(0,0,2.0/(right-left))
        S1.set(1,1,2.0/(top-bottom))
        return S1

    def __setT2(self):
        T2 = matrix(np.identity(4))
        T2.set(0,3,1.0)
        T2.set(1,3,1.0)
        return T2

    def __setS2(self,width,height):
        S2 = matrix(np.identity(4))
        S2.set(0,0,width/2.0)
        S2.set(1,1,height/2.0)
        return S2

    def __setW2(self,height):
        W2 = matrix(np.identity(4))
        W2.set(1,1,-1.0)
        W2.set(1,3,height)
        return W2

    def worldToViewingCoordinates(self,P):
        return self.__Mv*P

    def worldToImageCoordinates(self,P):
        return self.__M*P

    def worldToPixelCoordinates(self,P):
        return self.__M*P.scalarMultiply(1.0/(self.__M*P).get(3,0))

    def viewingToImageCoordinates(self,P):
        return self.__C*P

    def viewingToPixelCoordinates(self,P):
        return self.__C*P.scalarMultiply(1.0/(self.__C*P).get(3,0))

    def imageToPixelCoordinates(self,P):
        return P.scalarMultiply(1.0/P.get(3,0))

    def getUP(self):
        return self.__UP

    def getU(self):
        return self.__U

    def getV(self):
        return self.__V

    def getN(self):
        return self.__N

    def getMv(self):
        return self.__Mv

    def getC(self):
        return self.__C

    def getM(self):
        return self.__M

    def getNp(self):
        return self.__np

    def getFp(self):
        return self.__fp

    def setNp(self, nearPlane):
        self.__np = nearPlane

    def setFp(self, farPlane):
        self.__fp = farPlane
