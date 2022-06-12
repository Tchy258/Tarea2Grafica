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
        projection = tr.ortho(-8, 8, -4.5, 4.5, 0.1, 100)
    else:
        projection = tr.perspective(45, float(width)/float(height), 0.1, 300)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)


def setView(pipeline, mvpPipeline,controller):
    if controller.IsOrtho:
        controller.view = tr.lookAt(
            np.array([-4,10.,-5]),
            np.array([0,-10.,0]),
            np.array([1, 0.,1.])
        )
    
    else:
        controller.view = tr.lookAt(
            controller.camPos,
            controller.camPos+controller.camFront,
            np.array([0., 1., 0.])
        )

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, controller.view)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        pipeline.shaderProgram, "view"), 1, GL_TRUE, controller.view)

def createScene(pipeline):
    #Creacion del nodo raiz
    scene = sg.SceneGraphNode('system')
    #Nodo hijo que contiene los grupos de casas, no hay una transformación común a todas las casas así que tiene la identidad
    houses= sg.SceneGraphNode('houses')
    houses.transform = tr.identity()
    scene.childs+=[houses]

    #Nodo hijo del nodo houses que tiene un grupo de casas
    houseGroup= sg.SceneGraphNode('houseGroup1')
    houseGroup.transform = tr.identity()
    houses.childs+=[houseGroup]

    #Creacion de las paredes del primer grupo de casas, como un prisma de base cuadrada
    shapeWalls = bs.createTextureCube()
    gpuWalls = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls)
    gpuWalls.fillBuffers(
        shapeWalls.vertices, shapeWalls.indices)
    gpuWalls.texture = es.textureSimpleSetup(
        getAssetPath("ladrillo1.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    #Nodo que contiene el gpuShape del primer grupo de paredes, todas estas tienen un escalado y una traslación
    #que cumple función de "offset" respecto al origen
    walls = sg.SceneGraphNode('wallGroup1')
    walls.transform = tr.matmul([tr.translate(1.5, 0.0, 1.5),tr.scale(0.9,0.5,0.5)])
    walls.childs += [gpuWalls]

    #Imaginando el grupo de casas como un tablero de ajedrez equiespaciado, para las casas en el rango
    #([0,2],[1,3])
    for i in range(2):
        for j in range(6):
            #Se crea un nodo para sus paredes
            node = sg.SceneGraphNode('wall1.'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i-0.21, 0.3, -1.5*j),tr.scale(1.2,1,1)])
            node.childs += [walls]
            houseGroup.childs += [node]
            #Y otro para el segundo piso
            if i%2==0:
                node = sg.SceneGraphNode('secondFloor1'+str(i))
                node.transform = tr.matmul([tr.translate(-1.8*i, 0.8, -1.5*j)])
                node.childs += [walls]
                houseGroup.childs += [node]

    #Creacion de los techos
    shapeRoof = bs.createTexturePyramid()
    gpuRoof = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRoof)
    gpuRoof.fillBuffers(
        shapeRoof.vertices, shapeRoof.indices)
    gpuRoof.texture = es.textureSimpleSetup(
        getAssetPath("tejado1.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    #Estos deben ser ligeramente más anchos que las casas, y se escalan según ello
    roofs = sg.SceneGraphNode('roofGroup1')
    roofs.transform = tr.matmul([tr.translate(1.5, 0.0, 1.5),tr.scale(1.1,0.5,0.7)])
    roofs.childs += [gpuRoof]

    for i in range(2):
        for j in range(6):
            node = sg.SceneGraphNode('roof1.'+str(i))
            if i%2==0:
                node.transform = tr.matmul([tr.translate(-1.8*i, 1.305, -1.5*j)])
                node2=sg.SceneGraphNode('roof2extra'+str(i))
                node2.transform = tr.matmul([tr.translate(-1.8*i+1.653, 0.625, -1.5*j),tr.scale(0.24,0.3,1),tr.shearing(-1.08,0,0)])
                node2.childs+=[roofs]
                houseGroup.childs+=[node2]
            else:
                node.transform = tr.matmul([tr.translate(-1.8*i-0.2, 0.805, -1.5*j),tr.scale(1.2,1,1)])
            node.childs += [roofs]
            houseGroup.childs += [node]

    houseGroup= sg.SceneGraphNode('houseGroup2')
    houseGroup.transform = tr.identity()
    houses.childs+=[houseGroup]

    shapeWalls = bs.createTextureCube()
    gpuWalls = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls)
    gpuWalls.fillBuffers(
        shapeWalls.vertices, shapeWalls.indices)
    gpuWalls.texture = es.textureSimpleSetup(
        getAssetPath("ladrillo2.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    walls = sg.SceneGraphNode('wallGroup2')
    walls.transform = tr.matmul([tr.translate(1.5, 0.0, 1.5),tr.scale(0.9,0.5,0.5)])
    walls.childs += [gpuWalls]

    for i in range(2,4):
        for j in range(6):
            #Se crea un nodo para sus paredes
            node = sg.SceneGraphNode('wall2'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i, 0.3, -1.5*j),tr.scale(1.2,1,1)])
            node.childs += [walls]
            houseGroup.childs += [node]
            if i%2==0:
                node = sg.SceneGraphNode('secondFloor2'+str(i))
                node.transform = tr.matmul([tr.translate(-1.8*i+0.21, 0.8, -1.5*j)])
                node.childs += [walls]
                houseGroup.childs += [node]
    
    shapeRoof = bs.createTexturePyramid()
    gpuRoof = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRoof)
    gpuRoof.fillBuffers(
            shapeRoof.vertices, shapeRoof.indices )
    gpuRoof.texture = es.textureSimpleSetup(
        getAssetPath("tejado2.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    roofs = sg.SceneGraphNode('roofGroup2')
    roofs.transform = tr.matmul([tr.translate(1.5, 0.0, 1.5),tr.scale(1.1,0.5,0.7)])
    roofs.childs += [gpuRoof]

    for i in range(2,4):
        for j in range(6):
            node = sg.SceneGraphNode('roof2'+str(i))
            if i%2==0:
                node.transform = tr.matmul([tr.translate(-1.8*i+0.22, 1.305, -1.5*j)])
                node2=sg.SceneGraphNode('roof2extra'+str(i))
                node2.transform = tr.matmul([tr.translate(-1.8*i+1.865, 0.625, -1.5*j),tr.scale(0.24,0.3,1),tr.shearing(-1.08,0,0)])
                node2.childs+=[roofs]
                houseGroup.childs+=[node2]
            else:
                node.transform = tr.matmul([tr.translate(-1.8*i, 0.805, -1.5*j),tr.scale(1.2,1,1)])
            node.childs += [roofs]
            houseGroup.childs += [node]
    
    houseGroup= sg.SceneGraphNode('houseGroup3')
    houseGroup.transform = tr.identity()
    houses.childs+=[houseGroup]

    shapeWalls = bs.createTextureCube()
    gpuWalls = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls)
    gpuWalls.fillBuffers(
        shapeWalls.vertices, shapeWalls.indices)
    gpuWalls.texture = es.textureSimpleSetup(
        getAssetPath("ladrillo3.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    walls = sg.SceneGraphNode('wallGroup3')
    walls.transform = tr.matmul([tr.translate(1.5, 0.0, 1.5),tr.scale(0.9,0.5,0.5)])
    walls.childs += [gpuWalls]

    for i in range(4,6):
        for j in range(6):
            #Se crea un nodo para sus paredes
            node = sg.SceneGraphNode('wall3'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i, 0.3, -1.5*j),tr.scale(1.2,1,1)])
            node.childs += [walls]
            houseGroup.childs += [node]
            if i%2==0:
                node = sg.SceneGraphNode('secondFloor3'+str(i))
                node.transform = tr.matmul([tr.translate(-1.8*i+0.2, 0.8, -1.5*j)])
                node.childs += [walls]
                houseGroup.childs += [node]
    
    shapeRoof = bs.createTexturePyramid()
    gpuRoof = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRoof)
    gpuRoof.fillBuffers(
            shapeRoof.vertices, shapeRoof.indices )
    gpuRoof.texture = es.textureSimpleSetup(
        getAssetPath("tejado3.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    roofs = sg.SceneGraphNode('roofGroup3')
    roofs.transform = tr.matmul([tr.translate(1.5, 0.0, 1.5),tr.scale(1.1,0.5,0.7)])
    roofs.childs += [gpuRoof]

    for i in range(4,6):
        for j in range(6):
            node = sg.SceneGraphNode('roof3'+str(i))
            if i%2==0:
                node.transform = tr.matmul([tr.translate(-1.8*i+0.22, 1.305, -1.5*j)])
                node2=sg.SceneGraphNode('roof2extra'+str(i))
                node2.transform = tr.matmul([tr.translate(-1.8*i+1.865, 0.625, -1.5*j),tr.scale(0.24,0.3,1),tr.shearing(-1.08,0,0)])
                node2.childs+=[roofs]
                houseGroup.childs+=[node2]
            else:
                node.transform = tr.matmul([tr.translate(-1.8*i-0.02, 0.805, -1.5*j),tr.scale(1.2,1,1)])
            node.childs += [roofs]
            houseGroup.childs += [node]


    shapeFloor = bs.createTextureCube()
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.fillBuffers(
        shapeFloor.vertices, shapeFloor.indices)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("piso.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    fieldNode = sg.SceneGraphNode('floor')
    fieldNode.transform = tr.matmul(
        [tr.translate(1.5, 0.0, 1.5), tr.scale(1.8,0.1,1.5)])
    fieldNode.childs += [gpuFloor]

    for i in range(6):
        for j in range(6):
            node = sg.SceneGraphNode('tile'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i, 0.0, -1.5*j)])
            node.childs += [fieldNode]
            scene.childs += [node]

    return scene