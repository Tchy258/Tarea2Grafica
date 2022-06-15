from OpenGL.GL import *
import numpy as np
import constants

SIZE_IN_BYTES = constants.SIZE_IN_BYTES

#La clase GPUShape guarda la información de vertices para cargar el VAO, el VBO y el EBO
#en un shader
class GPUShape:
    def __init__(self):
        self.vao = None
        self.vbo = None
        self.ebo = None
        self.texture = None
        self.size = None
    #Inicialización de buffers según VAO, VBO y EBO
    def initBuffers(self):
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        return self

    def __str__(self):
        return "vao=" + str(self.vao) +\
            "  vbo=" + str(self.vbo) +\
            "  ebo=" + str(self.ebo) +\
            "  tex=" + str(self.texture)
    
    #Envío de información
    def fillBuffers(self, vertexData, indexData):

        vertexData = np.array(vertexData, dtype=np.float32)
        indexData = np.array(indexData, dtype=np.uint32)

        self.size = len(indexData)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(vertexData) * SIZE_IN_BYTES, vertexData, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indexData) * SIZE_IN_BYTES, indexData, GL_STATIC_DRAW)

    #Liberación de memoria
    def clear(self):
        
        if self.texture != None:
            glDeleteTextures(1, [self.texture])
            
        if self.ebo != None:
            glDeleteBuffers(1, [self.ebo])

        if self.vbo != None:
            glDeleteBuffers(1, [self.vbo])

        if self.vao != None:
            glDeleteVertexArrays(1, [self.vao])