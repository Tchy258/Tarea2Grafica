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
        projection = tr.ortho(-32, 32, -18, 18, 0.1, 100)
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
            np.array([0,10.,0]),
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
    scene.transform=tr.matmul([tr.translate(-5,0,-5),tr.rotationY(-np.pi)])
    #Nodo hijo que contiene los grupos de casas, no hay una transformación común a todas las casas así que tiene la identidad
    houses= sg.SceneGraphNode('houses')
    houses.transform = tr.translate(-1.2,0,0)
    scene.childs+=[houses]

    #Nodo hijo del nodo houses que tiene un grupo de casas
    houseGroup= sg.SceneGraphNode('houseGroup1')
    houseGroup.transform = tr.translate(0.5,0,0)
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
    walls.transform = tr.scale(1,0.5,0.5)
    walls.childs += [gpuWalls]

    #Imaginando el grupo de casas como un tablero de ajedrez equiespaciado
    for i in range(3):
        for j in range(10):
            #Se crea un nodo para sus paredes
            node = sg.SceneGraphNode('wall1.'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i, 0.3, -1.5*j),tr.scale(1.2,1,1)])
            node.childs += [walls]
            houseGroup.childs += [node]
            #Y otro para el segundo piso
            if i%2==0:
                node = sg.SceneGraphNode('secondFloor1'+str(i))
                node.transform = tr.matmul([tr.translate(-1.8*i, 0.8, -1.5*j),tr.translate(0.1, 0, 0)])
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
    #Estas matrices se aplicaran a distintos tipos de techo
    techoEnderezado=tr.matmul([tr.scale(1.2,0.5,0.7)])
    techoMovido=tr.matmul([tr.scale(0.26,0.3,1),tr.scale(1.1,0.5,0.6),tr.rotationY(np.pi),tr.shearingTecho()])
    roofs.transform = tr.identity()
    roofs.childs += [gpuRoof]

    for i in range(3):
        for j in range(10):
            node = sg.SceneGraphNode('roof1.'+str(i))
            if i%2==0:
                node.transform = tr.matmul([tr.translate(-1.8*i+0.1, 1.301, -1.5*j),techoEnderezado])
                node2=sg.SceneGraphNode('roof2extra'+str(i))
                node2.transform = tr.matmul([tr.translate(-1.8*i-0.545, 0.625, -1.5*j),techoMovido])
                node2.childs+=[roofs]
                houseGroup.childs+=[node2]
            else:
                node.transform = tr.matmul([tr.translate(-1.8*i, 0.805, -1.5*j),tr.scale(1.2,1,1),techoEnderezado])
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
    walls.transform = tr.scale(1.2,0.5,0.7)
    walls.childs += [gpuWalls]

    for i in range(4,7):
        for j in range(9):
            #Se crea un nodo para sus paredes
            node = sg.SceneGraphNode('wall2'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i, 0.3, -1.5*j),tr.scale(1.2,1,1)])
            node.childs += [walls]
            houseGroup.childs += [node]
            if i%2==0:
                node = sg.SceneGraphNode('secondFloor2'+str(i))
                node.transform = tr.matmul([tr.translate(-1.8*i, 0.8, -1.5*j),tr.translate(-0.12, 0, 0)])
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
    roofs.transform = tr.identity()
    roofs.childs += [gpuRoof]
    techoEnderezado=tr.matmul([tr.scale(1.5,0.5,0.9)])
    techoMovido=tr.matmul([tr.scale(0.26,0.3,1),tr.scale(1.3,0.5,0.8),tr.shearingTecho()])

    for i in range(4,7):
        for j in range(9):
            node = sg.SceneGraphNode('roof2'+str(i))
            if i%2==0:
                node.transform = tr.matmul([tr.translate(-1.8*i-0.12, 1.305, -1.5*j),techoEnderezado])
                node2=sg.SceneGraphNode('roof2extra'+str(i))
                node2.transform = tr.matmul([tr.translate(-1.8*i+0.65, 0.625, -1.5*j),techoMovido])
                node2.childs+=[roofs]
                houseGroup.childs+=[node2]
            else:
                node.transform = tr.matmul([tr.translate(-1.8*i, 0.805, -1.5*j),techoEnderezado])
            node.childs += [roofs]
            houseGroup.childs += [node]
    
    houseGroup= sg.SceneGraphNode('houseGroup3')
    houseGroup.transform = tr.translate(-1.5,0,0)
    houses.childs+=[houseGroup]

    shapeWalls = bs.createTextureCube()
    gpuWalls = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls)
    gpuWalls.fillBuffers(
        shapeWalls.vertices, shapeWalls.indices)
    gpuWalls.texture = es.textureSimpleSetup(
        getAssetPath("ladrillo3.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    walls = sg.SceneGraphNode('wallGroup3')
    walls.transform = tr.scale(0.9,0.5,1)
    walls.childs += [gpuWalls]

    for i in range(8,10):
        for j in range(5):
            #Se crea un nodo para sus paredes
            node = sg.SceneGraphNode('wall3'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i, 0.3, -2.5*j),tr.scale(1.2,1,1.5)])
            node.childs += [walls]
            houseGroup.childs += [node]
            if i%2==0:
                node = sg.SceneGraphNode('secondFloor3'+str(i))
                node.transform = tr.matmul([tr.translate(-1.8*i, 0.8, -2.5*j)])
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
    roofs.transform = tr.identity()
    roofs.childs += [gpuRoof]
    techoEnderezado=tr.scale(1.4,0.6,1.6)
    techoMovido=tr.matmul([tr.scale(0.26,0.3,1),tr.scale(1.3,0.5,0.8),tr.shearingTecho()])

    for i in range(8,10):
        for j in range(5):
            node = sg.SceneGraphNode('roof3'+str(i))
            if i%2==0:
                node.transform = tr.matmul([tr.translate(-1.8*i, 1.305, -2.5*j),techoEnderezado])
                node2=sg.SceneGraphNode('roof2extra'+str(i))
                node2.transform = tr.matmul([tr.translate(-1.8*i+1.865, 0.625, -2.5*j),techoMovido])
                node2.childs+=[roofs]
                houseGroup.childs+=[node2]
            else:
                node.transform = tr.matmul([tr.translate(-1.8*i, 0.852, -2.5*j),techoEnderezado])
            node.childs += [roofs]
            houseGroup.childs += [node]

    shapeDoor = bs.createDoor1()
    gpuDoor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuDoor)
    gpuDoor.fillBuffers(
        shapeDoor.vertices, shapeDoor.indices)
    gpuDoor.texture = es.textureSimpleSetup(
        getAssetPath("puerta1.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    doors=sg.SceneGraphNode("doorType1")
    doors.transform=tr.scale(0.22,0.44,0.04)
    doors.childs+=[gpuDoor]
    group1=sg.findNode(houses,"houseGroup1")
    group2=sg.findNode(houses,"houseGroup2")
    group3=sg.findNode(houses,"houseGroup3")

    for i in range(3):
        for j in range(10):
            node = sg.SceneGraphNode('doorType1'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i, 0.28, -1.5*j+0.25)])
            node.childs += [doors]
            group1.childs += [node]

    
    shapeLock = bs.createTextureCilinder(15)
    gpuLock = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuLock)
    gpuLock.fillBuffers(
        shapeLock.vertices, shapeLock.indices)
    gpuLock.texture = es.textureSimpleSetup(
        getAssetPath("chapa.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    locks=sg.SceneGraphNode("locks1")
    locks.transform=tr.matmul([tr.scale(0.01,0.01,0.024)])
    locks.childs+=[gpuLock]

    for i in range(3):
        for j in range(10):
            node = sg.SceneGraphNode('locks1'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i-0.09, 0.25, -1.5*j+0.25)])
            node.childs += [locks]
            group1.childs += [node]

    shapeDoor = bs.createDoor2()
    gpuDoor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuDoor)
    gpuDoor.fillBuffers(
        shapeDoor.vertices, shapeDoor.indices)
    gpuDoor.texture = es.textureSimpleSetup(
        getAssetPath("puerta2.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    doors=sg.SceneGraphNode("doorType2")
    doors.transform=tr.scale(0.18,0.36,0.03)
    doors.childs+=[gpuDoor]

    for i in range(4,7):
        for j in range(9):
            node = sg.SceneGraphNode('doorType2'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i-0.2, 0.22, -1.5*j+0.35)])
            node.childs += [doors]
            group2.childs += [node]

    shapeFloor = bs.createTextureCube()
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.fillBuffers(
        shapeFloor.vertices, shapeFloor.indices)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("piso.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    fieldNode = sg.SceneGraphNode('floor')
    fieldNode.transform = tr.matmul(
        [tr.translate(1.5, 0.0, 1.5), tr.scale(2,0.1,1.5)])
    fieldNode.childs += [gpuFloor]

    for i in range(16):
        for j in range(16):
            if i!=8 and i!=4:
                node = sg.SceneGraphNode('tile'+str(i))
                node.transform = tr.matmul([tr.translate(-2*i, 0.0, -1.5*j)])
                node.childs += [fieldNode]
                scene.childs += [node]

    return scene