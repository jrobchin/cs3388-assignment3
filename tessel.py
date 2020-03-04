import numpy as np
from matrix import matrix

from typing import Tuple

from cameraMatrix import cameraMatrix
from lightSource import lightSource
from object import object

class tessel:

    def __init__(self,objectTuple:Tuple[object],camera:cameraMatrix,light:lightSource):
        self.__faceList = [] #List of faces with attributes
        EPSILON = 0.001

        #Transform light position into viewing coordinates
        Lv = camera.worldToViewingCoordinates(light.getPosition())

        for object in objectTuple:
            u = object.getURange()[0]
            while u + object.getUVDelta()[0] < object.getURange()[1]  + EPSILON:
                v = object.getVRange()[0]
                while v + object.getUVDelta()[1] < object.getVRange()[1] + EPSILON:

                    #Collect surface points and transform them into viewing coordinates
                    facePointsWorld = [
                        object.getT()*object.getPoint(u, v),
                        object.getT()*object.getPoint(u+object.getUVDelta()[0], v),
                        object.getT()*object.getPoint(u+object.getUVDelta()[0], v+object.getUVDelta()[1]),
                        object.getT()*object.getPoint(u, v+object.getUVDelta()[1]),
                    ]
                    facePoints = [camera.worldToViewingCoordinates(fpw) for fpw in facePointsWorld]

		            #Compute vector elements necessary for face shading
                    C = self.__centroid(facePoints) #Find centroid point of face
                    N = self.__vectorNormal(facePoints) #Find normal vector to face
                    S = self.__vectorToLightSource(Lv,C) #Find vector to light source
                    R = self.__vectorSpecular(S,N) #Find specular reflection vector
                    V = self.__vectorToCentroid(C) #Find vector from surface centroid to origin of viewing coordinates

                    p_a, p_d, p_s, f = object.getReflectance()
                    #If surface is not a back face
                    if int(N.get(2, 0)) >= 0:
                    	#Compute face shading 
                        I_d = max(0, (S.removeRow(3).transpose() * N.removeRow(3)).get(0, 0) / (S.removeRow(3).norm() * N.removeRow(3).norm()))
                        I_s = max(0, (R.removeRow(3).transpose() * V.removeRow(3)).get(0, 0) / (R.removeRow(3).norm() * V.removeRow(3).norm()))

                        shading_coeff = (p_a + p_d * I_d + p_s * I_s ** f)
                        shading_color = [int(shading_coeff*c) for c in object.getColor()]
                    else:
                        shading_color = [int(p_a*c) for c in object.getColor()]

                    shading_color = tuple(shading_color)

                    #Transform 3D points expressed in viewing coordinates into 2D pixel coordinates
                    facePointsPixel = [camera.viewingToPixelCoordinates(fp) for fp in facePoints]

                    #Add the surface to the face list. Each list element is composed of the following items:
                    #[depth of the face centroid point (its Z coordinate), list of face points in pixel coordinates, face shading]
                    self.__faceList.append((C.get(2, 0), facePointsPixel, shading_color))

                    v += object.getUVDelta()[1]
                u += object.getUVDelta()[0]

    def __centroid(self,facePoints):
        #Returns the column matrix containing the face centroid point
        c_x = sum([pt.get(0, 0) for pt in facePoints]) / len(facePoints)
        c_y = sum([pt.get(1, 0) for pt in facePoints]) / len(facePoints)
        c_z = sum([pt.get(2, 0) for pt in facePoints]) / len(facePoints)
        return matrix(np.array([c_x, c_y, c_z, 1]).reshape(-1, 1))
 
    def __vectorNormal(self,facePoints):
        #Returns the column matrix containing the normal vector to the face.
        a = facePoints[0] - facePoints[2]
        b = facePoints[1] - facePoints[3]
        a = a.removeRow(3).transpose()
        b = b.removeRow(3).transpose()
        normal = a.crossProduct(b).transpose()
        return normal.insertRow(3, 1)

    def __vectorToLightSource(self,L,C):
        #Returns the column matrix containing the vector from the centroid to the light source
        return L - C

    def __vectorSpecular(self,S,N:matrix):
        #Returns the column matrix containing the vector of specular reflection
        a = (S.removeRow(3).transpose() * N.removeRow(3)).get(0, 0)
        b = N.removeRow(3).norm()**2
        c = a / b
        d = matrix(2 * c * N.removeRow(3).getArray())
        return (-S.removeRow(3) + d).insertRow(3, 1)

    def __vectorToCentroid(self,C):
        #Returns the column matrix containing the vector from the face centroid point to the origin of the viewing coordinates
        return -C

    def getFaceList(self): 
        #Returns the face list ready for drawing
        return self.__faceList