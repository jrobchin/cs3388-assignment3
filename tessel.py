import numpy as np
from matrix import matrix

class tessel:

    def __init__(self,objectTuple,camera,light):
        self.__faceList = [] #List of faces with attributes
        EPSILON = 0.001

        #Transform light position into viewing coordinates

        for object in objectTuple:
            u = object.getURange()[0]
            while u + object.getUVDelta()[0] < object.getURange()[1]  + EPSILON:
                v = object.getVRange()[0]
                while v + object.getUVDelta()[1] < object.getVRange()[1] + EPSILON:

                    #Collect surface points and transform them into viewing coordinates

		    #Compute vector elements necessary for face shading

                    C = self.__centroid(facePoints) #Find centroid point of face
                    N = self.__vectorNormal(facePoints) #Find normal vector to face
                    S = self.__vectorToLightSource(Lv,C) #Find vector to light source
                    R = self.__vectorSpecular(S,N) #Find specular reflection vector
                    V = self.__vectorToCentroid(C) #Find vector from surface centroid to origin of viewing coordinates

		    #If surface is not a back face

                    	#Compute face shading 

                    	#Transform 3D points expressed in viewing coordinates into 2D pixel coordinates

		    	#Add the surface to the face list. Each list element is composed of the following items:
		        #[depth of the face centroid point (its Z coordinate), list of face points in pixel coordinates, face shading]

                    v += object.getUVDelta()[1]
                u += object.getUVDelta()[0]

    def __centroid(self,facePoints):
        
    #Returns the column matrix containing the face centroid point
 
    def __vectorNormal(self,facePoints):

    #Returns the column matrix containing the normal vector to the face.

    def __vectorToLightSource(self,L,C):

    #Returns the column matrix containing the vector from the centroid to the light source

    def __vectorSpecular(self,S,N):

    #Returns the column matrix containing the vector of specular reflection

    def __vectorToCentroid(self,C):
    
    #Returns the column matrix containing the vector from the face centroid point to the origin of the viewing coordinates

    def getFaceList(self): #Returns the face list ready for drawing
        return self.__faceList