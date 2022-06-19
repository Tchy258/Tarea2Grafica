#Este archivo es donde se crean la mayoría de objetos
from pyparsing import traceParseAction
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
    #Se elijieron 40 y 22.5 para mantener la relación de aspecto 16:9
    if controller.IsOrtho:
        projection = tr.ortho(-40, 40, -22.5,22.5 , 0.1, 100)
    else:
        projection = tr.perspective(45, float(width)/float(height), 0.1, 300)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

#Función que cambia la vista según se esta en el modo ortogfrafico o en perspectiva
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

#Función que crea todo el grafo de escena
def createScene(pipeline):
    #Creacion del nodo raiz
    scene = sg.SceneGraphNode('system')
    #Nodo hijo que contiene los grupos de casas, no hay una transformación común a todas las casas así que tiene la identidad
    houses= sg.SceneGraphNode('houses')
    houses.transform = tr.translate(-1.2,0,0)
    scene.childs+=[houses]

    #Nodo hijo del nodo houses que tiene un grupo de casas
    houseGroup= sg.SceneGraphNode('houseGroup1')
    #houseGroup.transform = tr.translate(0.5,0,0)
    houses.childs+=[houseGroup]

    #Creacion de las paredes del primer grupo de casas, como un prisma de base cuadrada
    #shapeWalls = bs.createTextureCube()
    #gpuWalls = es.GPUShape().initBuffers()
    #pipeline.setupVAO(gpuWalls)
    #gpuWalls.fillBuffers(
    #    shapeWalls.vertices, shapeWalls.indices)
    #gpuWalls.texture = es.textureSimpleSetup(
    #    getAssetPath("ladrillo1.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    #Nodo que contiene el gpuShape del primer grupo de paredes, todas estas tienen un escalado y una traslación
    #que cumple función de "offset" respecto al origen
    #walls = sg.SceneGraphNode('wallGroup1')
    #walls.transform = tr.scale(1,0.5,0.5)
    #walls.childs += [gpuWalls]
    gpuList=[setupWalls(pipeline,"ladrillo1.jpg"),setupRoof(pipeline,"tejado1.jpg"), \
            setupDoor(pipeline,"puerta1.jpg"),setupLock(pipeline),setupWindow(pipeline,"ventana1.png"), \
            setupRoof2(pipeline,"tejado1.jpg") ]
    #Imaginando el grupo de casas como un tablero de ajedrez equiespaciado
    for i in range(3):
        for j in range(13):
            #Se crea un nodo para sus paredes
            if i%2==0:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,1.8*i,1.5*j,2)
                houseGroup.childs += [node]
            else:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,1.8*i,1.5*j,1)
                houseGroup.childs += [node]
            #Y otro para el segundo piso

    #Creacion de los techos
    #shapeRoof = bs.createTexturePyramid()
    #gpuRoof = es.GPUShape().initBuffers()
    #pipeline.setupVAO(gpuRoof)
    #gpuRoof.fillBuffers(
    #    shapeRoof.vertices, shapeRoof.indices)
    #gpuRoof.texture = es.textureSimpleSetup(
    #    getAssetPath("tejado1.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    #Estos deben ser ligeramente más anchos que las casas, y se escalan según ello
    #roofs = sg.SceneGraphNode('roofGroup1')
    #Estas matrices se aplicaran a distintos tipos de techo
    #techoEnderezado=tr.matmul([tr.scale(1.2,0.5,0.7)])
    #techoMovido=tr.matmul([tr.scale(0.26,0.3,1),tr.scale(1.1,0.5,0.6),tr.rotationY(np.pi),tr.shearingTecho()])
    #roofs.transform = tr.identity()
    #roofs.childs += [gpuRoof]

    #for i in range(3):
    #    for j in range(13):
    #        node = sg.SceneGraphNode('roof1.'+str(i))
    #        if i%2==0:
    #            node.transform = tr.matmul([tr.translate(-1.8*i+0.1, 1.301, -1.5*j),techoEnderezado])
    #            node2=sg.SceneGraphNode('roof1extra'+str(i))
    #            node2.transform = tr.matmul([tr.translate(-1.8*i-0.545, 0.625, -1.5*j),techoMovido])
    #            node2.childs+=[roofs]
    #            houseGroup.childs+=[node2]
    #        else:
    #            node.transform = tr.matmul([tr.translate(-1.8*i, 0.805, -1.5*j),tr.scale(1.2,1,1),techoEnderezado])
    #        node.childs += [roofs]
    #        houseGroup.childs += [node]

    #Otro nodo para agrupar casas
    houseGroup= sg.SceneGraphNode('houseGroup2')
    houseGroup.transform = tr.identity()
    houses.childs+=[houseGroup]
    #Mismos objetos anteriores con texturas diferentes y variaciones para el 
    #segundo lote de casas
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
        for j in range(13):
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
        for j in range(13):
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
    
    #Tercer grupo de casas
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

    for i in range(8,10):
        for j in range(5):
            node = sg.SceneGraphNode('roof3'+str(i))
            if i%2==0:
                node.transform = tr.matmul([tr.translate(-1.8*i, 1.305, -2.5*j),techoEnderezado])
            else:
                node.transform = tr.matmul([tr.translate(-1.8*i, 0.852, -2.5*j),techoEnderezado])
            node.childs += [roofs]
            houseGroup.childs += [node]

    #Se procede a hacer la creación de puertas, chapas y ventanas
    shapeDoor = bs.createDoor1()
    gpuDoor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuDoor)
    gpuDoor.fillBuffers(
        shapeDoor.vertices, shapeDoor.indices)
    gpuDoor.texture = es.textureSimpleSetup(
        getAssetPath("puerta1.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    doors=sg.SceneGraphNode("doorGroup1")
    doors.transform=tr.scale(0.22,0.44,0.04)
    doors.childs+=[gpuDoor]
    group1=sg.findNode(houses,"houseGroup1")
    group2=sg.findNode(houses,"houseGroup2")
    group3=sg.findNode(houses,"houseGroup3")

    for i in range(3):
        for j in range(13):
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

    locks=sg.SceneGraphNode("lockGroup1")
    locks.transform=tr.matmul([tr.scale(0.01,0.01,0.024)])
    locks.childs+=[gpuLock]

    for i in range(3):
        for j in range(13):
            node = sg.SceneGraphNode('locks1'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i-0.09, 0.25, -1.5*j+0.25)])
            node.childs += [locks]
            group1.childs += [node]

    shapeWindow = bs.createWindow1()
    gpuWindow = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWindow)
    gpuWindow.fillBuffers(
        shapeWindow.vertices, shapeWindow.indices)
    gpuWindow.texture = es.textureSimpleSetup(
        getAssetPath("ventana1.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    windows=sg.SceneGraphNode("windowGroup1")
    windows.transform=tr.scale(0.33,0.22,0.04)
    windows.childs+=[gpuWindow]

    for i in range(3):
        for j in range(13):
            node = sg.SceneGraphNode('windows1FirstFloor1'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i-0.6, 0.25, -1.5*j),tr.rotationY(np.pi/2)])
            node.childs += [windows]
            group1.childs += [node]
            node = sg.SceneGraphNode('windows1FirstFloor2'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i, 0.28, -1.5*j-0.25),tr.scale(1.5,1.5,1)])
            node.childs += [windows]
            group1.childs += [node]
            if i%2==0:
                node = sg.SceneGraphNode('windows1SecondFloor1'+str(i))
                node.transform = tr.matmul([tr.translate(-1.8*i-0.4, 0.85, -1.5*j),tr.rotationY(np.pi/2)])
                node.childs += [windows]
                group1.childs += [node]
                node = sg.SceneGraphNode('windows1SecondFloor1'+str(i))
                node.transform = tr.matmul([tr.translate(-1.8*i+0.2, 0.85, -1.5*j+0.25)])
                node.childs += [windows]
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
        for j in range(13):
            node = sg.SceneGraphNode('doorType2'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i-0.2, 0.22, -1.5*j+0.35)])
            node.childs += [doors]
            group2.childs += [node]
        
    shapeLock = bs.createTextureCilinder(15)
    gpuLock = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuLock)
    gpuLock.fillBuffers(
        shapeLock.vertices, shapeLock.indices)
    gpuLock.texture = es.textureSimpleSetup(
        getAssetPath("chapa.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    locks=sg.SceneGraphNode("lockGroup2")
    locks.transform=tr.matmul([tr.scale(0.01,0.01,0.022)])
    locks.childs+=[gpuLock]

    for i in range(4,7):
        for j in range(13):
            node = sg.SceneGraphNode('locks2'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i-0.27, 0.24, -1.5*j+0.35)])
            node.childs += [locks]
            group2.childs += [node]
    
    shapeWindow = bs.createWindow2()
    gpuWindow = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWindow)
    gpuWindow.fillBuffers(
        shapeWindow.vertices, shapeWindow.indices)
    gpuWindow.texture = es.textureSimpleSetup(
        getAssetPath("ventana2.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    windows=sg.SceneGraphNode("windowGroup2")
    windows.transform=tr.scale(0.33,0.22,0.04)
    windows.childs+=[gpuWindow]

    for i in range(4,7):
        for j in range(13):
            node = sg.SceneGraphNode('windows2FirstFloor1'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i-0.72, 0.25, -1.5*j),tr.rotationY(np.pi/2)])
            node.childs += [windows]
            group2.childs += [node]
            node = sg.SceneGraphNode('windows2FirstFloor2'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i, 0.28, -1.5*j-0.36),tr.scale(1.5,1.5,1)])
            node.childs += [windows]
            group2.childs += [node]
            if i%2==0:
                node = sg.SceneGraphNode('windows2SecondFloor1'+str(i))
                node.transform = tr.matmul([tr.translate(-1.8*i-0.72, 0.85, -1.5*j),tr.rotationY(np.pi/2)])
                node.childs += [windows]
                group2.childs += [node]
                node = sg.SceneGraphNode('windows2SecondFloor2'+str(i))
                node.transform = tr.matmul([tr.translate(-1.8*i+0.2, 0.85, -1.5*j+0.35)])
                node.childs += [windows]
                group2.childs += [node]

    shapeDoor = bs.createDoor2()
    gpuDoor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuDoor)
    gpuDoor.fillBuffers(
        shapeDoor.vertices, shapeDoor.indices)
    gpuDoor.texture = es.textureSimpleSetup(
        getAssetPath("puerta3.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    doors=sg.SceneGraphNode("doorType3")
    doors.transform=tr.scale(0.18,0.36,0.03)
    doors.childs+=[gpuDoor]

    for i in range(8,10):
        for j in range(5):
            node = sg.SceneGraphNode('doorType3'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i, 0.22, -2.5*j-0.75)])
            node.childs += [doors]
            group3.childs += [node]

    shapeLock = bs.createTextureCilinder(15)
    gpuLock = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuLock)
    gpuLock.fillBuffers(
        shapeLock.vertices, shapeLock.indices)
    gpuLock.texture = es.textureSimpleSetup(
        getAssetPath("chapa.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    locks=sg.SceneGraphNode("lockGroup3")
    locks.transform=tr.matmul([tr.scale(0.01,0.01,0.02)])
    locks.childs+=[gpuLock]

    for i in range(8,10):
        for j in range(5):
            node = sg.SceneGraphNode('locks3'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i-1.55, 0.22, -2.5*j-0.75)])
            node.childs += [locks]
            group2.childs += [node]

    shapeWindow = bs.createWindow1()
    gpuWindow = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWindow)
    gpuWindow.fillBuffers(
        shapeWindow.vertices, shapeWindow.indices)
    gpuWindow.texture = es.textureSimpleSetup(
        getAssetPath("ventana3.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    windows=sg.SceneGraphNode("windowGroup3")
    windows.transform=tr.scale(0.33,0.22,0.04)
    windows.childs+=[gpuWindow]

    for i in range(8,10):
        for j in range(5):
            node = sg.SceneGraphNode('windows3FirstFloor1'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i, 0.25, -2.5*j+0.75)])
            node.childs += [windows]
            group3.childs += [node]
            node = sg.SceneGraphNode('windows3FirstFloor2'+str(i))
            node.transform = tr.matmul([tr.translate(-1.8*i+0.55, 0.28, -2.5*j),tr.rotationY(np.pi/2),tr.scale(2,1.5,1)])
            node.childs += [windows]
            group3.childs += [node]
            if i%2==0:
                node = sg.SceneGraphNode('windows3SecondFloor1'+str(i))
                node.transform = tr.matmul([tr.translate(-1.8*i-0.45, 0.75, -2.5*j),tr.rotationY(np.pi/2)])
                node.childs += [windows]
                group3.childs += [node]
                node = sg.SceneGraphNode('windows3SecondFloor2'+str(i))
                node.transform = tr.matmul([tr.translate(-1.8*i, 0.75, -2.5*j-0.5)])
                node.childs += [windows]
                group3.childs += [node]
    
    #Se crea el piso de la calle
    shapeFloor = bs.createTextureCube()
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.fillBuffers(
        shapeFloor.vertices, shapeFloor.indices)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("piso.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    #Agregandolo a un nodo que representa al entorno de la escena
    environment = sg.SceneGraphNode("Environment")
    scene.childs+=[environment]
    floors = sg.SceneGraphNode('floor')
    floors.transform = tr.matmul(
        [tr.scale(2,0.1,1.5)])
    floors.childs += [gpuFloor]

    for i in range(1,12):
        for j in range(15):
            #En i=8 e i=4 iran pistas de autos
            if i!=8 and i!=4:
                if i<9:
                    node = sg.SceneGraphNode('tile'+str(i))
                    node.transform = tr.matmul([tr.translate(-2*i, 0.0, -1.5*j),tr.translate(1.5, 0.0, 1.5)])
                    node.childs += [floors]
                    environment.childs += [node]
                else:
                    if j<9:
                        node = sg.SceneGraphNode('tile'+str(i))
                        node.transform = tr.matmul([tr.translate(-2*i, 0.0, -1.5*j),tr.translate(1.5, 0.0, 1.5)])
                        node.childs += [floors]
                        environment.childs += [node]

    #Se crea la zona de pasto
    shapeGrass = bs.createTexturePyramid()
    gpuGrass = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGrass)
    gpuGrass.fillBuffers(
        shapeGrass.vertices,shapeGrass.indices)
    gpuGrass.texture=es.textureSimpleSetup (
        getAssetPath("pasto.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    grass = sg.SceneGraphNode('grass')
    grass.transform = tr.matmul([tr.translate(-2*8-0.6,0,-1.4*12-0.4),tr.translate(-1.9, 0.05, 1.5),tr.rotationY(np.pi),tr.rotationX(np.pi/2),tr.scale(6,8.9,0.1),tr.shearingTecho()])
    grass.childs+=[gpuGrass]
    environment.childs+=[grass]

    #Pistas de auto
    shapeRoad = bs.createTextureCube()
    gpuRoad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRoad)
    gpuRoad.fillBuffers(
        shapeRoad.vertices, shapeRoad.indices)
    gpuRoad.texture = es.textureSimpleSetup(
        getAssetPath("pista.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    #En sentido "vertical" según la proyección ortografica
    roads = sg.SceneGraphNode('roadV')
    roads.transform = tr.matmul(
        [tr.translate(1.5, 0.0, 1.5), tr.scale(2,0.1,1.5),tr.rotationY(np.pi/2)])
    roads.childs+=[gpuRoad]
    for j in range(15):
            if j<9:
                node = sg.SceneGraphNode('roadTile'+str(12))
                node.transform = tr.matmul([tr.translate(-2*12, 0.0, -1.5*j)])
                node.childs += [roads]
                environment.childs += [node]
            node = sg.SceneGraphNode('roadTile'+str(4))
            node.transform = tr.matmul([tr.translate(-2*4, 0.0, -1.5*j)])
            node.childs += [roads]
            environment.childs += [node]
            node = sg.SceneGraphNode('roadTile'+str(8))
            node.transform = tr.matmul([tr.translate(-2*8, 0.0, -1.5*j)])
            node.childs += [roads]
            environment.childs += [node]
            node = sg.SceneGraphNode('roadTile'+str(0))
            node.transform = tr.matmul([tr.translate(-2*0, 0.0, -1.5*j)])
            node.childs += [roads]
            environment.childs += [node]
    #En sentido "horizontal"
    roads = sg.SceneGraphNode('roadH')
    roads.transform = tr.matmul(
        [tr.translate(1.5, 0.0, 1.5), tr.scale(2,0.1,1.5)])
    roads.childs+=[gpuRoad]
    for i in range(13):
        if i<9:
            node = sg.SceneGraphNode('roadTile'+str(15))
            node.transform = tr.matmul([tr.translate(-2*i, 0.0, -1.5*15)])
            node.childs += [roads]
            environment.childs += [node]
        node = sg.SceneGraphNode('roadTile'+str(-1))
        node.transform = tr.matmul([tr.translate(-2*i, 0.0, -1.5*-1)])
        node.childs += [roads]
        environment.childs += [node]
    #Pista en diagonal
    roadGroup = sg.SceneGraphNode('roadGroup')
    roadGroup.transform=tr.matmul([tr.translate(-22.4,0,-10.69),tr.rotationY(0.99365)])
    environment.childs+=[roadGroup]
    roads = sg.SceneGraphNode('roadD')
    roads.transform = tr.matmul(
        [ tr.scale(2.05,0.1,1.24)])
    roads.childs+=[gpuRoad]
    for i in range(7):
        node = sg.SceneGraphNode('roadTile'+str(-1))
        node.transform = tr.matmul([tr.translate(2.05*i,0,0)])
        node.childs += [roads]
        roadGroup.childs += [node]

    return scene

def setupWalls(pipeline,imgName):
    shapeWalls = bs.createTextureCube()
    gpuWalls = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls)
    gpuWalls.fillBuffers(
        shapeWalls.vertices, shapeWalls.indices)
    gpuWalls.texture = es.textureSimpleSetup(
        getAssetPath(imgName), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    return gpuWalls

def setupRoof(pipeline,imgName):
    shapeRoof = bs.createTexturePyramid()
    gpuRoof = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRoof)
    gpuRoof.fillBuffers(
        shapeRoof.vertices, shapeRoof.indices)
    gpuRoof.texture = es.textureSimpleSetup(
        getAssetPath(imgName), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    return gpuRoof

def setupRoof2(pipeline,imgName):
    shapeRoof = bs.createTextureTrapezoid()
    gpuRoof = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRoof)
    gpuRoof.fillBuffers(
        shapeRoof.vertices, shapeRoof.indices)
    gpuRoof.texture = es.textureSimpleSetup(
        getAssetPath(imgName), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    return gpuRoof

def setupDoor(pipeline,name):
    shapeDoor =bs.createDoor1() if name=="puerta1.jpg" else bs.createDoor2()
    gpuDoor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuDoor)
    gpuDoor.fillBuffers(
        shapeDoor.vertices, shapeDoor.indices)
    gpuDoor.texture = es.textureSimpleSetup(
        getAssetPath(name), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    return gpuDoor

def setupLock(pipeline):
    shapeLock = bs.createTextureCilinder(15)
    gpuLock = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuLock)
    gpuLock.fillBuffers(
        shapeLock.vertices, shapeLock.indices)
    gpuLock.texture = es.textureSimpleSetup(
        getAssetPath("chapa.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    return gpuLock

def setupWindow(pipeline,name):
    shapeWindow = bs.createWindow2() if name=="ventana2.png" else bs.createWindow1()
    gpuWindow = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWindow)
    gpuWindow.fillBuffers(
        shapeWindow.vertices, shapeWindow.indices)
    gpuWindow.texture = es.textureSimpleSetup(
        getAssetPath(name), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    return gpuWindow

def setupFloor(pipeline):
    shapeFloor = bs.createTextureCube()
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.fillBuffers(
        shapeFloor.vertices, shapeFloor.indices)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("piso.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    return gpuFloor

def setupGrass(pipeline):
    shapeGrass = bs.createTexturePyramid()
    gpuGrass = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGrass)
    gpuGrass.fillBuffers(
        shapeGrass.vertices,shapeGrass.indices)
    gpuGrass.texture=es.textureSimpleSetup (
        getAssetPath("pasto.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    return gpuGrass

def setupRoad(pipeline):
    shapeRoad = bs.createTextureCube()
    gpuRoad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRoad)
    gpuRoad.fillBuffers(
        shapeRoad.vertices, shapeRoad.indices)
    gpuRoad.texture = es.textureSimpleSetup(
        getAssetPath("pista.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    return gpuRoad

def createHouseNode(name,gpuList,posX,posZ,type):
    nodoCasa = sg.SceneGraphNode(name)
    nodoCasa.transform=tr.translate(posX,0.2,posZ)

    wall=gpuList[0]
    nodoParedes=sg.SceneGraphNode(name + " walls")
    nodoParedes.childs+=[wall]
    nodoParedes.transform=tr.matmul([tr.translate(0,0.2,0),tr.scale(0.5,0.5,1)])
    nodoCasa.childs+=[nodoParedes]
    roof=gpuList[1]
    nodoTecho=sg.SceneGraphNode(name + " roof")
    nodoTecho.childs+=[roof]
    nodoTecho.transform=tr.matmul([tr.translate(0,0.7,0),tr.scale(0.75,0.45,1.5)])
    nodoCasa.childs+=[nodoTecho]
    door=gpuList[2]
    nodoPuerta=sg.SceneGraphNode(name + " door")
    nodoMarco=sg.SceneGraphNode(name + " door")
    nodoMarco.childs+=[door]
    nodoMarco.transform=tr.matmul([tr.translate(0.25,0.2,0.1),tr.rotationY(np.pi/2),tr.scale(0.22,0.44,0.04)])
    lock=gpuList[3]
    nodoChapa=sg.SceneGraphNode(name + " chapa")
    nodoChapa.childs+=[lock]
    nodoChapa.transform=tr.matmul([tr.translate(0.25,0.17,0.1885),tr.rotationY(np.pi/2),tr.scale(0.01,0.01,0.024)])
    nodoCasa.childs+=[nodoChapa]
    nodoPuerta.childs+=[nodoMarco,nodoChapa]
    nodoCasa.childs+=[nodoPuerta]
    window=gpuList[4]
    nodoVentana1=sg.SceneGraphNode(name + " window1")
    nodoVentana1.childs+=[window]
    nodoVentana1.transform=tr.matmul([tr.translate(-0.25,0.25,0),tr.rotationY(-np.pi/2),tr.scale(0.33,0.22,0.04)])
    nodoCasa.childs+=[nodoVentana1]
    nodoVentana2=sg.SceneGraphNode(name + " window2")
    nodoVentana2.childs+=[window]
    nodoVentana2.transform=tr.matmul([tr.translate(0,0.25,-0.49),tr.scale(0.33,0.22,0.04)])
    nodoCasa.childs+=[nodoVentana2]

    if type==2:
        nodoSegundoPiso=sg.SceneGraphNode(name + " second floor")
        nodoSegundoPiso.childs+=[wall]
        nodoSegundoPiso.transform=tr.matmul([tr.translate(0,0.7005,0),tr.scale(0.5,0.5,0.8)])
        nodoCasa.childs+=[nodoSegundoPiso]
        roof2=gpuList[5]
        nodoTecho=sg.findNode(nodoCasa,name + " roof")
        nodoTecho.transform=tr.matmul([tr.translate(0,1.09,0),tr.scale(0.75,0.45,1)])
        nodoTecho2=sg.SceneGraphNode(name + " second roof")
        nodoTecho2.childs+=[roof2]
        nodoTecho2.transform=tr.matmul([tr.translate(0,0.55,1),tr.rotationY(np.pi),tr.scale(0.6,0.2,0.2)])
        nodoCasa.childs+=[nodoTecho2]
        nodoTecho3=sg.SceneGraphNode(name + " third roof")
        nodoTecho3.childs+=[roof2]
        nodoTecho3.transform=tr.matmul([tr.translate(0,0.55,-1),tr.scale(0.6,0.2,0.2)])
        nodoCasa.childs+=[nodoTecho3]


    return nodoCasa