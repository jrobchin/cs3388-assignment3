from math import *
import numpy as np
from matrix import matrix

class transform(matrix):

    def __init__(self):
        super().__init__(np.identity(4))

    def translate(self,T):
        self.set(0,3,T.get(0,0))
        self.set(1,3,T.get(1,0))
        self.set(2,3,T.get(2,0))
        return self

    def scale(self,S):
        self.set(0,0,S.get(0,0))
        self.set(1,1,S.get(1,0))
        self.set(2,2,S.get(2,0))
        return self

    def rotate(self,A,angle):
        A = A.normalize()
        V = matrix(np.zeros((4,4)))
        V.set(0,1,-A.get(2,0))
        V.set(0,2,A.get(1,0))
        V.set(1,0,A.get(2,0))
        V.set(1,2,-A.get(0,0))
        V.set(2,0,-A.get(1,0))
        V.set(2,1,A.get(0,0))
        I = matrix(np.identity(4))
        self.setArray((I + V.scalarMultiply(sin(angle)) + (V*V).scalarMultiply(1.0-cos(angle))).getArray())
        return self