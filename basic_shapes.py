#Archivo basic_shapes.py del auxiliar 4

import numpy as np
from OpenGL.GL import *
import constants

SIZE_IN_BYTES = constants.SIZE_IN_BYTES

#Clase shape para contener vertices e indices
class Shape:
    def __init__(self, vertexData, indexData):
        self.vertexData = vertexData
        self.indexData = indexData

def createSphere(N, r, g, b):

    vertexData=[]

    indexData = []
    #Se definen un dphi y un dtheta para la arista del triangulo que forma el exterior de la esfera
    dphi = 2 * np.pi / N
    dtheta=np.pi/N
    r2=r
    g2=g
    b2=b
    R=1

    #Por cada espacio dtheta y phi, se asignan vertices basados en coordenadas esfericas que formaran la cara exterior de la esfera
    for i in range(N+1):
        theta =np.pi/2 - i * dtheta
        z=R*np.sin(theta)
        xy=R*np.cos(theta)
        for j in range(N+1):
            phi=j*dphi
            x=xy*np.cos(phi)
            y=xy*np.sin(phi)

            #Distribucion de colores

            if j%6==0:
                r2=r
                g2=g/8
                b2=b/4
            if j%6==1:
                r2=r/8
                g2=g
                b2=b/4
            if j%6==2:
                r2=r/4
                g2=g/8
                b2=b
            if j%6==3:
                r2=r
                g2=g/4
                b2=b/8
            if j%6==4:
                r2=r/4
                g2=g
                b2=b/8
            if j%6==5:
                r2=r/8
                g2=g/4
                b2=b

            vertexData += [
                # pos    # color
                x, y, z, r2, g2, b2
            ]
    
    #La esfera esta formada por multiples discos los cuales están conectados entre ellos con triangulos
    #dispuestos así /\/\/\ que van formar capas
    for j in range(1,((N+1)*(N+1)-N)+1):
        indexData+= [
            j-1,j+N,j+1
        ]
        indexData+= [
            j+1,j+N,j+N+1
        ]

    return Shape(vertexData, indexData)

def createPrism(width,depth,height,r,g,b):
    
    vertexData = np.array([
        # positions        # colors
        -width, -depth,  height,  r, g, b,
         width, -depth,  height,  r, g, b,
         width,  depth,  height,  r, g, b,
        -width,  depth,  height,  r, g, b,
 
        -width, -depth, -height,  r, g, b,
         width, -depth, -height,  r, g, b,
         width,  depth, -height,  r, g, b,
        -width,  depth, -height,  r, g, b
    ], dtype=np.float32)

    indexData = np.array([
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7
    ])

    return Shape(vertexData, indexData)

#Funcion para crear el cubo
def createCube():
    
    vertexData = np.array([
        # positions        # colors
        -0.5, -0.5,  0.5,  1.0, 0.0, 0.0,
         0.5, -0.5,  0.5,  0.0, 1.0, 0.0,
         0.5,  0.5,  0.5,  0.0, 0.0, 1.0,
        -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,
 
        -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,
         0.5, -0.5, -0.5,  0.0, 1.0, 0.0,
         0.5,  0.5, -0.5,  1.0, 0.0, 1.0,
        -0.5,  0.5, -0.5,  1.0, 1.0, 1.0
    ], dtype=np.float32)

    indexData = np.array([
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7
    ])

    return Shape(vertexData, indexData)
