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
    scene.childs+=[houses]

    #Nodo hijo del nodo houses que tiene un grupo de casas
    houseGroup1= sg.SceneGraphNode('houseGroup1')
    #houseGroup.transform = tr.translate(0.5,0,0)
    houses.childs+=[houseGroup1]

    
    gpuList=[setupGpu(pipeline,"ladrillo1.jpg"),setupGpu(pipeline,"tejado1.jpg"), \
            setupGpu(pipeline,"puerta1.jpg"),setupGpu(pipeline,"ventana1.png"), \
            setupRoof2(pipeline,"tejado1.jpg"),setupGpu(pipeline,"chapa.png") ]
    #Imaginando el grupo de casas como un tablero de ajedrez equiespaciado
    for i in range(-1,1,1):
        for j in range(10):
            #Se crea un nodo para sus paredes
            if j%2==1:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,1.5*i,1.5*j,2)
                houseGroup1.childs += [node]
            else:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,1.5*i,1.5*j,1)
                houseGroup1.childs += [node]
            #Y otro para el segundo piso

    

    #Otro nodo para agrupar casas
    houseGroup2= sg.SceneGraphNode('houseGroup2')
    houses.childs+=[houseGroup2]
    #Mismos objetos anteriores con texturas diferentes y variaciones para el 
    #segundo lote de casas
    gpuList=[setupGpu(pipeline,"ladrillo2.jpg"),setupGpu(pipeline,"tejado2.jpg"), \
            setupGpu(pipeline,"puerta2.png"),setupGpu(pipeline,"ventana2.png"), \
            setupRoof2(pipeline,"tejado2.jpg"),gpuList[-1] ]

    for i in range(3,5):
        for j in range(13):
            if j%2==1:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,-1.5*i,1.5*j,2)
                houseGroup2.childs += [node]
            else:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,-1.5*i,1.5*j,1)
                houseGroup2.childs += [node]
    

    #Tercer grupo de casas
    houseGroup3= sg.SceneGraphNode('houseGroup3')
    houses.childs+=[houseGroup3]

    gpuList=[setupGpu(pipeline,"ladrillo3.jpg"),setupGpu(pipeline,"tejado3.jpg"), \
            setupGpu(pipeline,"puerta3.png"),setupGpu(pipeline,"ventana3.png"), \
            setupRoof2(pipeline,"tejado3.jpg"),gpuList[-1] ]    
    

    for i in range(6,8):
        for j in range(13):
            if j%2==1:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,-1.5*i,1.5*j,2)
                houseGroup3.childs += [node]
            else:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,-1.5*i,1.5*j,1)
                houseGroup3.childs += [node]
    

    gpuFloor = setupGpu(pipeline,"piso.jpg")
    #Agregandolo a un nodo que representa al entorno de la escena
    environment = sg.SceneGraphNode("Environment")
    scene.childs+=[environment]
    floors = sg.SceneGraphNode('floorTiles')
    for i in range(-1,8,1):
        if i!=-1 and i!=2 and i!=5:
            stretch=createEnvNode("stretch " +str(i),gpuFloor,"V",13)
            stretch.transform=tr.matmul([tr.translate(-1.5*i,0,0),stretch.transform])
            floors.childs+=[stretch]

    environment.childs+=[floors]
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
    gpuRoad= setupGpu(pipeline,"pista.jpg")
    #En sentido "vertical" según la proyección ortografica
    roads=sg.SceneGraphNode('roads')
    roadsV = sg.SceneGraphNode('roadV')
    for i in range(-1,9,1):
        if i==-1 or i==2 or i==5 or i==8:
            stretch=createEnvNode("stretch " + str(i),gpuRoad,"V",13,"Road")
            stretch.transform=tr.matmul([tr.translate(-1.5*i,0,0),stretch.transform])
            roadsV.childs+=[stretch]
    roads.childs+=[roadsV]
    #En sentido "horizontal"
    roadsH = sg.SceneGraphNode('roadH')
    stretch=createEnvNode("stretch lower",gpuRoad,"H",8,"Road")
    stretch.transform=tr.matmul([tr.translate(-1.5*7,0,-1.5),stretch.transform])
    roadsH.childs+=[stretch]
    stretch=createEnvNode("stretch lower",gpuRoad,"H",8,"Road")
    stretch.transform=tr.matmul([tr.translate(-1.5*7,0,1.5*13),stretch.transform])
    roadsH.childs+=[stretch]
    roads.childs+=[roadsH]

    environment.childs+=[roads]
    

    return scene

def setupGpu(pipeline,imgName):
    fullName=imgName.split('.')
    name=fullName[0]
    name=name[:-1] if name[-1].isnumeric() else name
    if name=="ladrillo" or name=="piso" or name=="pista":
        shape = bs.createTextureCube()
    elif name=="tejado" or name=="pasto":
        shape = bs.createTexturePyramid()
    elif name=="ventana":
        shape= bs.createWindow2() if imgName=="ventana2.png" else bs.createWindow1()
    elif name=="puerta":
        shape = bs.createDoor1() if imgName=="puerta1.jpg" else bs.createDoor2()
    else:
        shape= bs.createTextureCilinder(15)
    gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu)
    gpu.fillBuffers(
        shape.vertices, shape.indices)
    gpu.texture = es.textureSimpleSetup(
        getAssetPath(imgName), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    return gpu


def setupRoof2(pipeline,imgName):
    shapeRoof = bs.createTextureTrapezoid()
    gpuRoof = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRoof)
    gpuRoof.fillBuffers(
        shapeRoof.vertices, shapeRoof.indices)
    gpuRoof.texture = es.textureSimpleSetup(
        getAssetPath(imgName), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    return gpuRoof


def createHouseNode(name,gpuList,posX,posZ,type):
    nodoCasa = sg.SceneGraphNode(name)
    nodoCasa.transform=tr.translate(posX,0.0965,posZ)

    wall=gpuList[0]
    nodoParedes=sg.SceneGraphNode(name + " walls")
    nodoParedes.childs+=[wall]
    nodoParedes.transform=tr.matmul([tr.translate(0,0.2,0),tr.scale(0.5,0.5,1)])
    nodoCasa.childs+=[nodoParedes]
    roof=gpuList[1]
    nodoTecho=sg.SceneGraphNode(name + " roof")
    nodoTecho.childs+=[roof]
    nodoTecho.transform=tr.matmul([tr.translate(0,0.65,0),tr.scale(0.75,0.45,1.3)])
    nodoCasa.childs+=[nodoTecho]
    door=gpuList[2]
    nodoPuerta=sg.SceneGraphNode(name + " door")
    nodoMarco=sg.SceneGraphNode(name + " door")
    nodoMarco.childs+=[door]
    nodoMarco.transform=tr.matmul([tr.translate(0.25,0.18,0.1),tr.rotationY(np.pi/2),tr.scale(0.22,0.44,0.04)])
    lock=gpuList[-1]
    nodoChapa=sg.SceneGraphNode(name + " chapa")
    nodoChapa.childs+=[lock]
    nodoChapa.transform=tr.matmul([tr.translate(0.25,0.15,0.1885),tr.rotationY(np.pi/2),tr.scale(0.01,0.01,0.024)])
    nodoCasa.childs+=[nodoChapa]
    nodoPuerta.childs+=[nodoMarco,nodoChapa]
    nodoCasa.childs+=[nodoPuerta]
    window=gpuList[3]
    nodoVentana1=sg.SceneGraphNode(name + " window1")
    nodoVentana1.childs+=[window]
    nodoVentana1.transform=tr.matmul([tr.translate(-0.25,0.25,0),tr.rotationY(-np.pi/2),tr.scale(0.33,0.22,0.04)])
    nodoCasa.childs+=[nodoVentana1]
    nodoVentana2=sg.SceneGraphNode(name + " window2")
    nodoVentana2.childs+=[window]
    nodoVentana2.transform=tr.matmul([tr.translate(0,0.25,-0.49),tr.scale(0.33,0.22,0.04)])
    nodoCasa.childs+=[nodoVentana2]
    nodoVentana3=sg.SceneGraphNode(name + " window3")
    nodoVentana3.childs+=[window]
    nodoVentana3.transform=tr.matmul([tr.translate(0,0.25,0.49),tr.scale(0.33,0.22,0.04)])
    nodoCasa.childs+=[nodoVentana3]

    if type==2:
        nodoSegundoPiso=sg.SceneGraphNode(name + " second floor")
        nodoSegundoPiso.childs+=[wall]
        nodoSegundoPiso.transform=tr.matmul([tr.translate(0,0.7005,0),tr.scale(0.5,0.5,0.8)])
        nodoCasa.childs+=[nodoSegundoPiso]
        roof2=gpuList[4]
        nodoTecho=sg.findNode(nodoCasa,name + " roof")
        nodoTecho.transform=tr.matmul([tr.translate(0,1.09,0),tr.scale(0.75,0.45,1)])
        nodoTecho2=sg.SceneGraphNode(name + " second roof")
        nodoTecho2.childs+=[roof2]
        nodoTecho2.transform=tr.matmul([tr.translate(0,0.55,0.5),tr.scale(0.6,0.2,0.2)])
        nodoCasa.childs+=[nodoTecho2]
        nodoTecho3=sg.SceneGraphNode(name + " third roof")
        nodoTecho3.childs+=[roof2]
        nodoTecho3.transform=tr.matmul([tr.translate(0,0.55,-0.5),tr.rotationY(np.pi),tr.scale(0.6,0.2,0.2)])
        nodoCasa.childs+=[nodoTecho3]
        nodoVentana4=sg.SceneGraphNode(name + " window4")
        nodoVentana4.childs+=[window]
        nodoVentana4.transform=tr.matmul([tr.translate(0.25,0.7,0),tr.rotationY(-np.pi/2),tr.scale(0.33,0.22,0.04)])
        nodoCasa.childs+=[nodoVentana4]
        nodoVentana5=sg.SceneGraphNode(name + " window5")
        nodoVentana5.childs+=[window]
        nodoVentana5.transform=tr.matmul([tr.translate(-0.25,0.7,0),tr.rotationY(-np.pi/2),tr.scale(0.33,0.22,0.04)])
        nodoCasa.childs+=[nodoVentana5]
    if int((posX/-1.5))%2==0:
        if posX>=-6 and posX<=-1:
            nodoCasa.transform=tr.matmul([tr.translate(posX,0.0965,posZ),tr.rotationY(np.pi)])
    elif int((posX/-1.5))%2==1: 
        if posX>=-2.2 or posX<=-8:
            nodoCasa.transform=tr.matmul([tr.translate(posX,0.0965,posZ),tr.rotationY(np.pi)])

    return nodoCasa

def createEnvNode(name,gpu,direction,length,type="Floor"):
    nodoPiso=sg.SceneGraphNode(name)
    for i in range(length):
        nodoCuadro=sg.SceneGraphNode(name + " tile " + str(i))
        nodoCuadro.transform=tr.matmul([tr.scale(1.5,0.1,1.5)])
        if direction=="V":
            if type=="Road" or "Grass":
                nodoCuadro.transform=tr.matmul([tr.translate(0,0,1.5*i),tr.rotationY(np.pi/2),nodoCuadro.transform])
            else:
                nodoCuadro.transform=tr.matmul([tr.translate(0,0,1.5*i),nodoCuadro.transform])
        else:
            nodoCuadro.transform=tr.matmul([tr.translate(1.5*i,0,0),nodoCuadro.transform])
        nodoCuadro.childs+=[gpu]
        nodoPiso.childs+=[nodoCuadro]
    return nodoPiso