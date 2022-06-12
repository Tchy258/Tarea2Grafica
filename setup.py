import transformations as tr
from OpenGL.GL import *
import numpy as np
import scene_graph as sg
import basic_shapes as bs
import easy_shaders as es
from assets_path import getAssetPath
#La función setProjection cambia la proyección en ambos shaders (textura y camara)
#de ortografica a perspectiva según corresponda
def setProjection(controller,pipeline, mvpPipeline, width, height):
    if controller.IsOrtho:
        projection = tr.ortho(-1, 1, -1, 1, 0.1, 100)
    else:
        projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)


def setView(pipeline, mvpPipeline,controller):
    if controller.IsOrtho:
        view = tr.lookAt(
            np.array([0.,5.,0.]),
            np.array([0.,-5.,0.]),
            np.array([0, 1.,0.])
        )
    
    else:
        view = tr.lookAt(
            controller.camPos,
            controller.camPos+controller.camFront,
            np.array([0., 1., 0.])
        )

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

def createScene(pipeline):
    shapeBrickCube = bs.createTextureCube()
    gpuBrickCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrickCube)
    gpuBrickCube.fillBuffers(
        shapeBrickCube.vertices, shapeBrickCube.indices)
    gpuBrickCube.texture = es.textureSimpleSetup(
        getAssetPath("ladrillo1.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    fieldNode = sg.SceneGraphNode('brickCube')
    fieldNode.transform = tr.matmul(
        [tr.translate(1.5, 0.0, 1.5), tr.scale(0.5,0.5,0.5), tr.translate(0.0, -0.5, 0.0)])
    fieldNode.childs += [gpuBrickCube]

    scene = sg.SceneGraphNode('system')
    scene.childs += [fieldNode]

    for i in range(7):
        for j in range(7):
            node = sg.SceneGraphNode('plane'+str(i))
            node.transform = tr.matmul([tr.translate(-0.6*i, 0.5, -0.6*j)])
            node.childs += [fieldNode]
            scene.childs += [node]

    return scene

def createMinecraftBlock():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+: block top
        0.5,  0.5,  0.5, 1/4, 2/3,
        0.5, -0.5,  0.5, 0, 2/3,
        -0.5, -0.5,  0.5, 0, 1/3,
        -0.5,  0.5,  0.5, 1/4, 1/3,

        # Z-: block bottom
        -0.5, -0.5, -0.5, 3/4, 1/3,
        0.5, -0.5, -0.5, 3/4, 2/3,
        0.5,  0.5, -0.5, 2/4, 2/3,
        -0.5,  0.5, -0.5, 2/4, 1/3,

        # X+: block left
        0.5, -0.5, -0.5, 2/4, 1,
        0.5,  0.5, -0.5, 2/4, 2/3,
        0.5,  0.5,  0.5, 1/4, 2/3,
        0.5, -0.5,  0.5, 1/4, 1,

        # X-: block right
        -0.5, -0.5, -0.5, 3/4, 2/3,
        -0.5,  0.5, -0.5, 2/4, 2/3,
        -0.5,  0.5,  0.5, 2/4, 1/3,
        -0.5, -0.5,  0.5, 3/4, 1/3,

        # Y+: white face
        -0.5,  0.5, -0.5, 2/4, 1/3,
        0.5,  0.5, -0.5, 2/4, 2/3,
        0.5,  0.5,  0.5, 1/4, 2/3,
        -0.5,  0.5,  0.5, 1/4, 1/3,

        # Y-: yellow face
        -0.5, -0.5, -0.5, 1, 1/3,
        0.5, -0.5, -0.5, 1, 2/3,
        0.5, -0.5,  0.5, 3/4, 2/3,
        -0.5, -0.5,  0.5, 3/4, 1/3
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return bs.Shape(vertices, indices)
