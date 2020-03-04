from math import *
import numpy as np
from matrix import matrix
from graphicsWindow import graphicsWindow
from cameraMatrix import cameraMatrix
from lightSource import lightSource
from transform import transform
from parametricPlane import parametricPlane
from parametricCircle import parametricCircle
from parametricSphere import parametricSphere
from parametricTorus import parametricTorus
from parametricCone import parametricCone
from parametricCylinder import parametricCylinder
from tessel import tessel

#Set up constants required for the camera and the rendering process
#Near and far planes
NP = 10.0
FP = 50.0

#Image size
WIDTH = 1800
HEIGHT = 840

#Image aspect
THETA = 45.0
ASPECT = WIDTH/HEIGHT

#Vector in the up direction
Px = 0.0
Py = 0.0
Pz = 1.0

#Position of camera
Ex = 120.0
Ey = 120.0
Ez = 40.0

#Gaze point
Gx = 0.0
Gy = 0.0
Gz = -40.0

#Light position
Lx = 10.0
Ly = 10.0
Lz = 30.0

#Light color
Lr = 1.0
Lg = 1.0
Lb = 1.0

#Light intensity
Ir = 1.0
Ig = 1.0
Ib = 1.0

P = matrix(np.ones((4,1))) #Up direction
E = matrix(np.ones((4,1))) #Origin of viewing coordinates
G = matrix(np.ones((4,1))) #Gaze point

#Set light position
L = matrix(np.ones((4,1)))
L.set(0,0,Lx)
L.set(1,0,Ly)
L.set(2,0,Lz)

#Set up light color
C = (Lr,Lg,Lb)

#Set up light intensity
I = (Ir,Ig,Ib)

#Set up the up vector
P.set(0,0,Px)
P.set(1,0,Py)
P.set(2,0,Pz)

#Set up the viewing point
E.set(0,0,Ex)
E.set(1,0,Ey)
E.set(2,0,Ez)

#Set up the gaze point
G.set(0,0,Gx)
G.set(1,0,Gy)
G.set(2,0,Gz)

#BEGIN PROGRAM HERE

#Create and position a plane
planeT = matrix(np.identity(4))
planeT.set(0,3,-40.0)
planeT.set(1,3,-40.0)
planeT.set(2,3,-40.0)
planeCol = (255,0,255)
planeRef = (0.2,0.4,0.4,10.0)
planeWidth = 100.0
planeLength = 100.0
plane = parametricPlane(planeT,planeWidth,planeLength,planeCol,planeRef,(0.0,1.0),(0.0,1.0),(1.0/10.0,1.0/10.0))

#Create an position a cone
coneT = matrix(np.identity(4))
coneT.set(0,3,50.0)
coneCol = (0,255,0)
coneRef = (0.2,0.4,0.4,10.0)
coneHeight = 20.0
coneRadius = 10.0
cone = parametricCone(coneT,coneHeight,coneRadius,coneCol,coneRef,(0.0,1.0),(0.0,2.0*pi),(1.0/10.0,pi/18.0))

#Create and position a sphere
sphereT = matrix(np.identity(4))
sphereT.set(0,3,30.0)
sphereCol = (255,255,0)
sphereRef = (0.2,0.4,0.4,10.0)
sphereRadius = 10.0
sphere = parametricSphere(sphereT,sphereRadius,sphereCol,sphereRef,(0.0,pi),(0.0,2.0*pi),(pi/64.0,2.0*pi/64.0))

#Create and position a cylinder
cylinderT = matrix(np.identity(4))
cylinderCol = (255,0,0)
cylinderRef = (0.2,0.4,0.4,10.0)
cylinderHeight = 20.0
cylinderRadius = 10.0
cylinder = parametricCylinder(cylinderT,cylinderHeight,cylinderRadius,cylinderCol,cylinderRef,(0.0,1.0),(0.0,2.0*pi),(1.0/10.0,pi/18.0))

#Create and position a cylinder top cap
topCircleT = matrix(np.identity(4))
topCircleT.set(2,3,20.0) #Elevate to the height of the cylinder
topCircleCol = (255,0,0)
topCircleRef = (0.2,0.4,0.4,10.0)
topCircleRadius = 10.0
topCircle = parametricCircle(topCircleT,topCircleRadius,topCircleCol,topCircleRef,(0.0,1.0),(0.0,2.0*pi),(1.0/10.0,pi/18.0))

#Create and position a cylinder bottom cap
bottomCircleT = matrix(np.identity(4))
bottomCircleCol = (255,0,0)
bottomCircleRef = (0.2,0.4,0.4,10.0)
bottomCircleRadius = 10.0
bottomCircle = parametricCircle(bottomCircleT,bottomCircleRadius,bottomCircleCol,bottomCircleRef,(0.0,1.0),(0.0,2.0*pi),(1.0/10.0,pi/18.0))

#Create and position a torus
torusT = matrix(np.identity(4))
torusT.set(0,3,50.0)
torusCol = (0,255,0)
torusRef = (0.2,0.4,0.4,10.0)
torusInnerRadius = 20.0
torusOuterRadius = 5.0
torus = parametricTorus(torusT,torusInnerRadius,torusOuterRadius,torusCol,torusRef,(0.0,2.0*pi),(0.0,2.0*pi),(2.0*pi/256.0,2.0*pi/64.0))

#Compose rotation transform for the cylinder and its caps around (1,1,1) by a non-zero angle

#Set vector for rotation
V = matrix(np.zeros((3,1)))
V.set(0,0,1.0)
V.set(1,0,1.0)
V.set(2,0,1.0)

#Set the rotation matrix for cylinder, its top, and its bottom caps
R1 = transform().rotate(V,pi/4.0)

#Set a rotation matrix to flip the bottom circle by 180 degrees such that the normals point in the right direction
V.set(0,0,1.0)
V.set(1,0,0.0)
V.set(2,0,0.0)
R2 = transform().rotate(V,pi)

#Apply transformations to objects in the correct order
cylinder.setT(R1*cylinder.getT())
bottomCircle.setT(R1*R2*bottomCircle.getT())
topCircle.setT(R1*topCircle.getT())

#Rotate the torus with the same rotation used for the cylinder
torus.setT(R1*torus.getT())

#Open a graphics window, set camera viewing system, and create light source
window = graphicsWindow(WIDTH,HEIGHT)
camera = cameraMatrix(P,E,G,NP,FP,WIDTH,HEIGHT,THETA) #Set camera viewing system
light = lightSource(L,C,I)

#Draw the list of face for the scene
window.drawFaces(tessel((cylinder,topCircle,bottomCircle,sphere,cone,torus,plane),camera,light).getFaceList())

window.saveImage("testImage.png")
window.showImage()