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

def createTexturePyramid():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        # Y-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5, -0.5,  0.5, 0, 1,
        -0.5, -0.5,  0.5, 1, 1,

        # Y+
        0.0,  0.5, 0.0, 0.5, 0,

        # Y-
        0.5, -0.5,  0.5, 1, 0,
        -0.5, -0.5,  0.5, 0, 0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 5, 5, 6, 0,  # Y-
        0, 4, 1, #Z-
        1, 4, 2, #X+
        2, 4, 3,
        3, 4 ,0
    ]

    return Shape(vertices, indices)
