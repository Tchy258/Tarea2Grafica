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

#Funcion auxiliar para calcular la normal de una superficie
def surfaceNormal(v1,v2,v3):
    #Vectores que determinan la superficie según los puntos del triángulo cuya normal se está calculando
    u=v2-v1 
    v=v3-v1
    normal=np.cross(u,v)
    normal/=np.linalg.norm(normal)
    #Si el producto punto entre la normal y cualquiera de los puntos es negativo
    if np.dot(normal,v1)<0:
        #Entonces esta normal apunta hacia "adentro", por lo que se busca la normal opuesta
        normal=-normal
    return normal

#Funcion auxiliar para calcular la normal de un vértice
def vertexNormal(normalArray):
    #La normal de un vértice se calcula como el promedio de las normales de las superficies a las que
    #el vértice pertenece
    average=np.array([0.,0.,0.])
    for i in range(len(normalArray)):
        average+=normalArray[i]
    average/=len(normalArray)
    return average.tolist()

#Funcion auxiliar para extraer los vertices de una lista de vertices de una funcion que retorna un shape
def extractVertices(shapeVertices):
    vertices=[]
    for i in range(0,len(shapeVertices),5):
        vertices+=[shapeVertices[i:i+3]]
    return vertices

#Funcion que dado una lista de listas que representan vertices, y sus indices, calcula las normales de cada vertice
def calculatePerVertexNormal(vertexList,indices):
    listOfVertexNormals=[]
    #Por cada vertice en la lista de vertices
    for i in range(len(vertexList)):
        surfaceNormals=[]
        #Revisar la lista de indices
        for j in range(len(indices)):
            #Si el vertice participa en la formación de este triángulo
            if indices[j]==i:
                #Ver cual vertice del triángulo es
                vertexPosition=j%3
                #Si es el inferior izquierdo
                if vertexPosition==0:
                    normal=surfaceNormal(np.array(vertexList[indices[j]]), \
                                                np.array(vertexList[indices[j+1]]), \
                                                np.array(vertexList[indices[j+2]]))
                #Inferior derecho
                elif vertexPosition==1:
                    normal=surfaceNormal(np.array(vertexList[indices[j-1]]), \
                                                np.array(vertexList[indices[j]]), \
                                                np.array(vertexList[indices[j+1]]))
                #Superior
                elif vertexPosition==2:
                    normal=surfaceNormal(np.array(vertexList[indices[j-2]]), \
                                                np.array(vertexList[indices[j-1]]), \
                                                np.array(vertexList[indices[j]]))
                #Luego se añade la normal calculada a la lista de normales de superficie para este vertice
                surfaceNormals+=[normal]
        #Una vez recorridos todos los indices, se calcula la normal del vertice y se agrega a la lista de normales
        normalAvg=vertexNormal(surfaceNormals)
        for j in range(3):
            listOfVertexNormals.append(normalAvg[j])
    return listOfVertexNormals


#Funcion auxiliar para insertar normales de vertices dada una lista de ellos proveniente de un shape y sus indices
def insertVertexNormals(vertices,indices):
    vertexList=extractVertices(vertices)
    normals=calculatePerVertexNormal(vertexList,indices)
    vertexArrayIndex=5
    normalArrayIndex=0
    while vertexArrayIndex<len(vertices):
        for j in range(normalArrayIndex,normalArrayIndex+3):
            vertices.insert(vertexArrayIndex+j%3,normals[j])
        normalArrayIndex+=3
        vertexArrayIndex+=8
    for j in range(len(normals)-3,len(normals)):
        vertices.append(normals[j])



#Funcion para crear un cubo con texturas y normales
def createTextureCubeWithNormals():

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

    #Insercion de normales
    insertVertexNormals(vertices,indices)

    return Shape(vertices, indices)

def createTextureTrapezoidWithNormals():

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

    insertVertexNormals(vertices,indices)

    return Shape(vertices, indices)

def createTexturePyramidWithNormals():

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

    insertVertexNormals(vertices,indices)

    return Shape(vertices, indices)

def createGrassWithNormals():

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
    
    insertVertexNormals(vertices,indices)

    return Shape(vertices, indices)

#Función para crear un cilindro texturizado de suavidad N, en particular se uso para las
#chapas de las puertas
def createTextureCilinderWithNormals(N,D):

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

    insertVertexNormals(vertexData,indexData)

    return Shape(vertexData, indexData)

#Funcion para crear la puerta1 con las coordenadas de textura correctas
#Es igual a la del cubo pero con distintas coordenadas
def createDoor1WithNormals():

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

    insertVertexNormals(vertices,indices)

    return Shape(vertices, indices)

#Lo mismo para la puerta 2
def createDoor2WithNormals():

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

    insertVertexNormals(vertices,indices)

    return Shape(vertices, indices)

#Funcion para crear la ventana1 con las coordenadas de textura correctas
def createWindow1WithNormals():

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

    insertVertexNormals(vertices,indices)

    return Shape(vertices, indices)

#Funcion para crear la ventana2 con las coordenadas de textura correctas
def createWindow2WithNormals():

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

    insertVertexNormals(vertices,indices)

    return Shape(vertices, indices)