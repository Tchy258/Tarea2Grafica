#Archivo basic_shapes.py del auxiliar 4

import numpy as np
from OpenGL.GL import *
import constants

SIZE_IN_BYTES = constants.SIZE_IN_BYTES

#Clase shape para contener vertices e indices
class Shape:
    def __init__(self, vertexData, indexData):
        self.vertices = vertexData
        self.indices = indexData

#Funcion para crear un cubo con texturas
def createTextureCube():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+
        -0.5, -0.5,  0.5, 0, 1,
        0.5, -0.5,  0.5, 1, 1,
        0.5,  0.5,  0.5, 1, 0,
        -0.5,  0.5,  0.5, 0, 0,

        # Z-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5,  0.5, -0.5, 1, 0,
        -0.5,  0.5, -0.5, 0, 0,

        # X+
        0.5, -0.5, -0.5, 0, 1,
        0.5,  0.5, -0.5, 0, 0,
        0.5,  0.5,  0.5, 1, 0,
        0.5, -0.5,  0.5, 1, 1,

        # X-
        -0.5, -0.5, -0.5, 0, 1,
        -0.5,  0.5, -0.5, 0, 0,
        -0.5,  0.5,  0.5, 1, 0,
        -0.5, -0.5,  0.5, 1, 1,

        # Y+
        -0.5,  0.5, -0.5, 0, 1,
        0.5,  0.5, -0.5, 1, 1,
        0.5,  0.5,  0.5, 1, 0,
        -0.5,  0.5,  0.5, 0, 0,

        # Y-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5, -0.5,  0.5, 1, 0,
        -0.5, -0.5,  0.5, 0, 0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 4, 5, 5, 6, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)

def createTextureTrapezoid():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+
        -0.5, -0.5,  0.5, 0, 1,
        0.5, -0.5,  0.5, 1, 1,
        0.375,  0.5,  -0.5, 3/4, 0,
        -0.375,  0.5,  -0.5, 0, 0,

        # Z-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.375,  0.5, -0.5, 3/4, 0,
        -0.375,  0.5, -0.5, 0, 0,

        # X+
        0.5, -0.5, -0.5, 0, 1,
        0.5,  -0.5, 0.5, 1, 1,
        0.375,  0.5,  -0.5, 0, 0.5,

        # X-
        -0.5, -0.5, -0.5, 0, 1,
        -0.5,  -0.5,  0.5, 1, 1,
        -0.375,  0.5, -0.5, 0, 0.5,


        # Y-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5, -0.5,  0.5, 1, 0,
        -0.5, -0.5,  0.5, 0, 0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 4, 5, 5, 6, 7,  # Z-
        8, 9, 10,   # X+
        11,12,13,  # X-
        14,15,16,16,17,14]  # Y-

    return Shape(vertices, indices)

def createTexturePyramid():

    vertices = [
        # Base
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5, -0.5,  0.5, 0, 1,
        -0.5, -0.5,  0.5, 1, 1,

        # Vertice superior
        0.0,  0.5, 0.0, 0.5, 0,

        # Vertices auxiliares para mapear bien texturas
        0.5, -0.5,  0.5, 1, 0,
        -0.5, -0.5,  0.5, 0, 0
    ]

    indices = [
        0, 1, 5, 5, 6, 0,  # Base
        0, 4, 1, #Caras laterales
        1, 4, 2, 
        2, 4, 3,
        3, 4 ,0
    ]

    return Shape(vertices, indices)

def createGrass():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+/X-
        -0.5, -0.5,  -0.5, 0, 1,
        -0.5, 0.5,  -0.5, 1, 1,
        0.5,  -0.5,  0.5, 1, 0,
        0.5,  0.5,  0.5, 0, 0,

        # Z-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5,  0.5, -0.5, 1, 0,
        -0.5,  0.5, -0.5, 0, 0,

        # X+
        0.5, -0.5, -0.5, 0, 1,
        0.5,  0.5, -0.5, 0, 0,
        0.5,  0.5,  0.5, 1, 0,
        0.5, -0.5,  0.5, 1, 1,

        # Y+
        -0.5,  0.5, -0.5, 0, 1,
        0.5,  0.5, -0.5, 1, 1,
        0.5,  0.5,  0.5, 1, 0,

        # Y-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5, -0.5,  0.5, 1, 0,
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 1,  # Z+/X-
        7, 4, 5, 5, 6, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        12, 13, 14,  # Y+
        15, 16, 17]  # Y-

    return Shape(vertices, indices)

#Función para crear un cilindro texturizado de suavidad N, en particular se uso para las
#chapas de las puertas
def createTextureCilinder(N,D):

    H=1
    vertexData=[0.,0.,-H, 1/2,1/2]
    indexData = []
    #Se define un dphi para las tapas del cilindro
    dphi = 2 * np.pi / N
    R=1
    z=-H
    #Vertices tapa inferior
    for i in range(D):
        phi=dphi*i
        x=R*np.cos(phi)
        y=R*np.sin(phi)
        vertexData += [
                # pos    # tex
                x, y, z, 1-(x+1)*0.5 , 1-(y+1)*0.5
            ]
    z=H
    #Vertices tapa superior
    for i in range(D):
        phi=dphi*i
        x=R*np.cos(phi)
        y=R*np.sin(phi)
        vertexData += [
                # pos    # tex
                x, y, z, 1-(x+1)*0.5 , 1-(y+1)*0.5
            ]
    vertexData+=[0.,0.,H, 1/2,1/2]
    
    #Indices tapa inferior
    for i in range(1,D):
        indexData+= [0,i,i+1]
    indexData+= [0,D,1]
    #Indices tapa superior
    for i in range(1,D):
        indexData+= [D+1,D+i,D+i+1]
    #Vertices laterales del cilindro
    for i in range(D+1):
        phi=dphi*i
        x=R*np.cos(phi)
        y=R*np.sin(phi)
        if i%2==0:
            #Vertices izquierdos del triangulo i
            vertexData += [
                    # pos    # tex
                    x, y, -H, 60/1055. , 398/1055.
                ]
            vertexData += [
                    # pos    # tex
                    x, y, H, 60/1055. , 352/1055.
                ]
        else:
            #Vertices derechos
            vertexData += [
                    # pos    # tex
                    x, y, -H, 112/1055. , 398/1055.
                ]
            vertexData += [
                    # pos    # tex
                    x, y, H, 112/1055. , 352/1055.
                ]
    #indices laterales del cilindro
    for i in range(2*D-4,len(vertexData),2):
        #|\
        #---
        indexData+= [
            i-1,i,i+1
        ]
        #---|
        # \ |
        indexData+= [
            i+1,i+2,i
        ]
    return Shape(vertexData, indexData)

#Funcion para crear la puerta1 con las coordenadas de textura correctas
#Es igual a la del cubo pero con distintas coordenadas
def createDoor1():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+
        -0.5, -0.5,  0.5, 0, 1,
        0.5, -0.5,  0.5, 1, 1,
        0.5,  0.5,  0.5, 1, 0,
        -0.5,  0.5,  0.5, 0, 0,

        # Z-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5,  0.5, -0.5, 1, 0,
        -0.5,  0.5, -0.5, 0, 0,

        # X+
        0.5, -0.5, -0.5, 813/900., 1,
        0.5,  0.5, -0.5, 813/900., 30/1800.,
        0.5,  0.5,  0.5, 1, 30/1800.,
        0.5, -0.5,  0.5, 1, 1,

        # X-
        -0.5, -0.5, -0.5, 813/900., 1,
        -0.5,  0.5, -0.5, 813/900., 30/1800.,
        -0.5,  0.5,  0.5, 1, 30/1800.,
        -0.5, -0.5,  0.5, 1, 1,

        # Y+
        -0.5,  0.5, -0.5, 813/900., 1,
        0.5,  0.5, -0.5, 1, 1,
        0.5,  0.5,  0.5, 1, 30/1900.,
        -0.5,  0.5,  0.5, 813/900., 30/1900.,

        # Y-
        -0.5, -0.5, -0.5, 813/900., 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5, -0.5,  0.5, 1, 30/1800.,
        -0.5, -0.5,  0.5, 813/900., 30/1900.
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 4, 5, 5, 6, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)

#Lo mismo para la puerta 2
def createDoor2():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+
        -0.5, -0.5,  0.5, 0, 1,
        0.5, -0.5,  0.5, 1, 1,
        0.5,  0.5,  0.5, 1, 0,
        -0.5,  0.5,  0.5, 0, 0,

        # Z-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5,  0.5, -0.5, 1, 0,
        -0.5,  0.5, -0.5, 0, 0,

        # X+
        0.5, -0.5, -0.5, 583/694., 1423/1500.,
        0.5,  0.5, -0.5, 583/694., 34/1500.,
        0.5,  0.5,  0.5, 655/694, 34/1500.,
        0.5, -0.5,  0.5, 655/694, 1423/1500.,

        # X-
        -0.5, -0.5, -0.5, 583/694., 1423/1500.,
        -0.5,  0.5, -0.5, 583/694., 34/1500.,
        -0.5,  0.5,  0.5, 655/694, 34/1500.,
        -0.5, -0.5,  0.5, 655/694, 1423/1500.,

        # Y+
        -0.5,  0.5, -0.5, 583/694., 1423/1500.,
        0.5,  0.5, -0.5, 655/694, 1423/1500.,
        0.5,  0.5,  0.5, 655/694, 30/1900.,
        -0.5,  0.5,  0.5, 583/694., 30/1900.,

        # Y-
        -0.5, -0.5, -0.5, 583/694., 1423/1500.,
        0.5, -0.5, -0.5, 655/694, 1423/1500.,
        0.5, -0.5,  0.5, 655/694, 34/1500.,
        -0.5, -0.5,  0.5, 583/694., 30/1900.
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 4, 5, 5, 6, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)

#Funcion para crear la ventana1 con las coordenadas de textura correctas
def createWindow1():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+
        -0.5, -0.5,  0.5, 0, 1,
        0.5, -0.5,  0.5, 1, 1,
        0.5,  0.5,  0.5, 1, 0,
        -0.5,  0.5,  0.5, 0, 0,

        # Z-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5,  0.5, -0.5, 1, 0,
        -0.5,  0.5, -0.5, 0, 0,

        # X+
        0.5, -0.5, -0.5, 0., 57/1335.,
        0.5,  0.5, -0.5, 0., 1172/1335.,
        0.5,  0.5,  0.5, 74/1801., 57/1335.,
        0.5, -0.5,  0.5, 74/1801., 1172/1335.,

        # X-
        -0.5, -0.5, -0.5, 0, 1172/1335.,
        -0.5,  0.5, -0.5, 0, 57/1335.,
        -0.5,  0.5,  0.5, 74/1801., 57/1335.,
        -0.5, -0.5,  0.5, 74/1801., 1172/1335.,

        # Y+
        -0.5,  0.5, -0.5, 0, 1172/1335.,
        0.5,  0.5, -0.5, 74/1801., 1172/1335.,
        0.5,  0.5,  0.5, 74/1801., 57/1335.,
        -0.5,  0.5,  0.5, 0, 57/1335.,

        # Y-
        -0.5, -0.5, -0.5, 0, 1172/1335.,
        0.5, -0.5, -0.5, 74/1801., 1172/1335.,
        0.5, -0.5,  0.5, 74/1801., 57/1335.,
        -0.5, -0.5,  0.5, 0, 57/1335.
    ]
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 4, 5, 5, 6, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)

#Funcion para crear la ventana2 con las coordenadas de textura correctas
def createWindow2():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+
        -0.5, -0.5,  0.5, 0, 1,
        0.5, -0.5,  0.5, 1, 1,
        0.5,  0.5,  0.5, 1, 0,
        -0.5,  0.5,  0.5, 0, 0,

        # Z-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5,  0.5, -0.5, 1, 0,
        -0.5,  0.5, -0.5, 0, 0,

        # X+
        0.5, -0.5, -0.5, 3/233., 19/393.,
        0.5,  0.5, -0.5, 3/233., 37/393.,
        0.5,  0.5,  0.5, 13/233., 19/393.,
        0.5, -0.5,  0.5, 13/233., 37/393.,

        # X-
        -0.5, -0.5, -0.5, 3/233., 37/393.,
        -0.5,  0.5, -0.5, 3/233., 19/393.,
        -0.5,  0.5,  0.5, 13/233., 19/393.,
        -0.5, -0.5,  0.5, 13/233., 37/393.,

        # Y+
        -0.5,  0.5, -0.5, 0, 37/393.,
        0.5,  0.5, -0.5, 13/233., 37/393.,
        0.5,  0.5,  0.5, 13/233., 19/393.,
        -0.5,  0.5,  0.5, 0, 19/393.,

        # Y-
        -0.5, -0.5, -0.5, 0, 37/393.,
        0.5, -0.5, -0.5, 13/233., 37/393.,
        0.5, -0.5,  0.5, 13/233., 19/393.,
        -0.5, -0.5,  0.5, 0, 19/393.
    ]
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 4, 5, 5, 6, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)