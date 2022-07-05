#Este archivo es donde se crean la mayoría de objetos
from os import system
from pyparsing import traceParseAction
from setuptools import setup
import grafica.transformations as tr
from OpenGL.GL import *
import numpy as np
import grafica.scene_graph as sg
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
from grafica.controller import Controller,Spotlight
from grafica.assets_path import getAssetPath



#La función setProjection dibuja lo que efectivamente se ve en pantalla, lo que ve la cámara
#y como se comportan las luces
def setProjection(controller,lightPipeline, texPipeline, width, height,spotlightsPool,theta,hora):
    #Se elijieron 40 y 22.5 para mantener la relación de aspecto 16:9
    if controller.IsOrtho:
        projection = tr.ortho(-40, 40, -22.5,22.5 , 0.1, 100)
    else:
        projection = tr.perspective(45, float(width)/float(height), 0.1, 300)
    #Si no está "prendida" la linterna
    if not controller.flashlightOn:
        #Sus valores de intensidad son 0
        spotlightsPool['spot1'].ambient = np.array([0, 0, 0])
        spotlightsPool['spot1'].diffuse = np.array([0., 0., 0.])
        spotlightsPool['spot1'].specular = np.array([0., 0., 0.])
    else:
        spotlightsPool['spot1'].ambient = np.array([0, 0, 0])
        spotlightsPool['spot1'].diffuse = np.array([1.0, 1.0, 1.0])
        spotlightsPool['spot1'].specular = np.array([1.0, 1.0, 1.0])

    #Dependiendo de la hora
    for i in range(2,40):
        #Se prenden o apagan las luces
        if hora>18 or hora<7:
            spotlightsPool['spot'+str(i)].ambient = np.array([0.0, 0.0, 0.0])
            spotlightsPool['spot'+str(i)].diffuse = np.array([0.6, 0.6, 0.6])
            spotlightsPool['spot'+str(i)].specular = np.array([0.6, 0.6, 0.6])
        else:
            spotlightsPool['spot'+str(i)].ambient = np.array([0, 0, 0])
            spotlightsPool['spot'+str(i)].diffuse = np.array([0., 0., 0.])
            spotlightsPool['spot'+str(i)].specular = np.array([0., 0., 0.])
    #Las del auto son más intensas
    for i in range(40,42):
        if hora>18 or hora<7:
            spotlightsPool['spot'+str(i)].ambient = np.array([0.0, 0.0, 0.0])
            spotlightsPool['spot'+str(i)].diffuse = np.array([1., 1., 1.])
            spotlightsPool['spot'+str(i)].specular = np.array([1., 1., 1.])
        else:
            spotlightsPool['spot'+str(i)].ambient = np.array([0, 0, 0])
            spotlightsPool['spot'+str(i)].diffuse = np.array([0., 0., 0.])
            spotlightsPool['spot'+str(i)].specular = np.array([0., 0., 0.])



    #Se fija la proyección en el shader de la cámara y de los objetos sin texturas
    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    #Estas luces puntuales representam al sol y la luna
    #El día y la noche se distinguen según el ángulo de rotación respecto al centro de la escena que tengan
    xSol=-6*np.cos(theta)
    ySol=30
    zSol=7*np.sin(theta)
    #La luz del sol es el máximo entre 0.7 más un factor que depende de su ángulo respecto al origen o 0
    ambientSol=max(0.7+0.5*np.cos(theta),0)
    xLuna=xSol
    yLuna=-ySol
    zLuna=zSol
    #Como la luna y el sol son opuestos, si el coseno es negativo para el sol, será positivo para la luna
    ambientLuna=max(0.001-0.05*np.cos(theta),0)
    #Actualización de parametros de las luces en el shader
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].ambient"), ambientSol, ambientSol, ambientSol)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].diffuse"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].specular"), 0.0, 0.0, 0.0)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].position"),xSol,ySol,zSol )

    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[1].ambient"), ambientLuna, ambientLuna, ambientLuna)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[1].diffuse"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[1].specular"), 0.0, 0.0, 0.0)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[1].constant"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[1].linear"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[1].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[1].position"),xLuna,yLuna,zLuna )

    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.diffuse"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "material.shininess"), 32)

    #Se envían las luces del diccionario spotLightspool al shader de luces
    for i, (k,v) in enumerate(spotlightsPool.items()):
        baseString = "spotLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "linear"), v.linear)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "quadratic"), v.quadratic)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)

    #Lo mismo para el shader de texturas
    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    

    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].ambient"), ambientSol, ambientSol, ambientSol)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].diffuse"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].specular"), 0.0, 0.0, 0.0)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].position"), xSol, ySol, zSol)

    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].ambient"), ambientLuna, ambientLuna, ambientLuna)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].diffuse"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].specular"), 0.0, 0.0, 0.0)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].constant"), 0.1)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].linear"), 0.1)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].position"), xLuna, yLuna, zLuna)

    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.diffuse"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "material.shininess"), 32)

    for i, (k,v) in enumerate(spotlightsPool.items()):
        baseString = "spotLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "linear"), v.linear)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "quadratic"), v.quadratic)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)


#Función que cambia la vista según se esta en el modo ortogfrafico o en perspectiva
def setView(lightPipeline,texPipeline,controller):
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

    Xesf = np.sin(controller.cameraPhiAngle)*np.cos(controller.cameraThetaAngle) #coordenada X esferica
    Zesf = np.sin(controller.cameraPhiAngle)*np.sin(controller.cameraThetaAngle) #coordenada Y esferica
    Yesf = np.cos(controller.cameraThetaAngle)

    #Posición de la vista
    viewPos = np.array([controller.camPos[0]-Xesf,controller.camPos[1]-Yesf,controller.camPos[2]-Zesf])

    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "view"), 1, GL_TRUE, controller.view)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])

    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "view"), 1, GL_TRUE, controller.view)


#Funciones tomadas del archivo "ex_obj_reader.py" del github del curso para leer archivos .obj
#Esta función corrobora que el obj esté bien formateado
def readFaceVertex(faceDescription):

    aux = faceDescription.split('/')

    assert len(aux[0]), "Vertex index has not been defined."

    faceVertex = [int(aux[0]), None, None]

    assert len(aux) == 3, "Only faces where its vertices require 3 indices are defined."

    if len(aux[1]) != 0:
        faceVertex[1] = int(aux[1])

    if len(aux[2]) != 0:
        faceVertex[2] = int(aux[2])

    return faceVertex


#Esta función lee el archivo obj y crea un gpuShape a partir de él con vértices e indices
def readOBJ(filename, color):

    vertices = []
    normals = []
    textCoords= []
    faces = []

    with open(filename, 'r') as file:
        for line in file.readlines():
            aux = line.strip().split(' ')
            
            if aux[0] == 'v':
                vertices += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vn':
                normals += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vt':
                assert len(aux[1:]) == 2, "Texture coordinates with different than 2 dimensions are not supported"
                textCoords += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'f':
                N = len(aux)                
                faces += [[readFaceVertex(faceVertex) for faceVertex in aux[1:4]]]
                for i in range(3, N-1):
                    faces += [[readFaceVertex(faceVertex) for faceVertex in [aux[i], aux[i+1], aux[1]]]]

        vertexData = []
        indices = []
        index = 0

        # Per previous construction, each face is a triangle
        for face in faces:

            # Checking each of the triangle vertices
            for i in range(0,3):
                vertex = vertices[face[i][0]-1]
                normal = normals[face[i][2]-1]

                vertexData += [
                    vertex[0], vertex[1], vertex[2],
                    color[0], color[1], color[2],
                    normal[0], normal[1], normal[2]
                ]

            # Connecting the 3 vertices to create a triangle
            indices += [index, index + 1, index + 2]
            index += 3        

        return bs.Shape(vertexData, indices)


#Función que crea todo lo que tiene texturas en la escena
def createScene(pipeline):
    #Creacion del nodo raiz
    scene = sg.SceneGraphNode('system')
    #Nodo hijo que contiene los grupos de casas, no hay una transformación común a todas las casas así que tiene la identidad
    houses= sg.SceneGraphNode('houses')
    scene.childs+=[houses]

    #Nodo hijo del nodo houses que tiene un grupo de casas
    houseGroup1= sg.SceneGraphNode('houseGroup1')
    houses.childs+=[houseGroup1]

    #Se crea una lisa de gpuShape para construir la casa
    gpuList=[setupGpu(pipeline,"ladrillo1.jpg"),setupGpu(pipeline,"tejado1.jpg"), \
            setupGpu(pipeline,"puerta1.jpg"),setupGpu(pipeline,"ventana1.png"), \
            setupRoof2(pipeline,"tejado1.jpg"),setupGpu(pipeline,"chapa.png") ]

    #Imaginando el grupo de casas como un tablero de ajedrez equiespaciado
    for i in range(-1,1,1):
        for j in range(10):
            #Se crean 20 casas de 3 tipos entre las coordenadas -1.5 y 0 del eje x
            t=j%3
            if t==1:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,1.5*i,1.5*j,2)
                houseGroup1.childs += [node]
            elif t==2:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,1.5*i,1.5*j,1)
                houseGroup1.childs += [node]
            elif t==0:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,1.5*i,1.5*j,3)
                houseGroup1.childs += [node]

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
            t=j%3
            if t==1:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,-1.5*i,1.5*j,3)
                houseGroup2.childs += [node]
            elif t==2:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,-1.5*i,1.5*j,1)
                houseGroup1.childs += [node]
            elif t==0:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,-1.5*i,1.5*j,2)
                houseGroup2.childs += [node]
    

    #Tercer grupo de casas
    houseGroup3= sg.SceneGraphNode('houseGroup3')
    houses.childs+=[houseGroup3]

    gpuList=[setupGpu(pipeline,"ladrillo3.jpg"),setupGpu(pipeline,"tejado3.jpg"), \
            setupGpu(pipeline,"puerta3.png"),setupGpu(pipeline,"ventana3.png"), \
            setupRoof2(pipeline,"tejado3.jpg"),gpuList[-1] ]    
    

    for i in range(6,8):
        for j in range(13):
            t=j%3
            if t==1:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,-1.5*i,1.5*j,2)
                houseGroup3.childs += [node]
            elif t==2:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,-1.5*i,1.5*j,3)
                houseGroup1.childs += [node]
            elif t==0:
                node=createHouseNode("house "+ str(i) + str(j),gpuList,-1.5*i,1.5*j,1)
                houseGroup3.childs += [node]
    
    #Piso
    gpuFloor = setupGpu(pipeline,"piso.jpg")
    #Agregandolo a un nodo que representa al entorno de la escena
    environment = sg.SceneGraphNode("Environment")
    scene.childs+=[environment]
    floors = sg.SceneGraphNode('floorTiles')
    #Se crean "filas" de cuadrados de piso (un stretch)
    for i in range(-1,8,1):
        if i!=-1 and i!=2 and i!=5:
            if i==0 or i==1:
                stretch=createEnvNode("stretch " +str(i),gpuFloor,"V",10)
            else:
                stretch=createEnvNode("stretch " +str(i),gpuFloor,"V",13)
            stretch.transform=tr.matmul([tr.translate(-1.5*i,0,0),stretch.transform])
            floors.childs+=[stretch]

    environment.childs+=[floors]
    #Se crea la zona de pasto con un piso subyacente que tiene la misma forma
    gpuGrass=setupGpu(pipeline,"pasto.jpg")
    grassTile=createEnvNode('grass node',gpuGrass,"C",1,"Pasto")
    grass = sg.SceneGraphNode('grass')
    grass.transform = tr.matmul([tr.translate(-0.75,0,1.5*11)])
    gpuFloor2=setupGpu(pipeline,"piso.jpg",2)
    floorUnderGrass = createEnvNode('floor node',gpuFloor2,"C",1)
    grass.childs+=[grassTile]
    grass.childs+=[floorUnderGrass]
    environment.childs+=[grass]

    #Pistas de auto
    gpuRoad= setupGpu(pipeline,"pista.jpg")
    #En sentido "vertical" según la proyección ortografica
    roads=sg.SceneGraphNode('roads')
    roadsV = sg.SceneGraphNode('roadV')
    for i in range(-1,9,1):
        if i==-1:
            stretch=createEnvNode("stretch " + str(i),gpuRoad,"V",11,"Road")
            stretch.transform=tr.matmul([tr.translate(-1.5*i,0,-1.5),stretch.transform])
            roadsV.childs+=[stretch]
        if i==2 or i==5 or i==8:
            stretch=createEnvNode("stretch " + str(i),gpuRoad,"V",13,"Road")
            stretch.transform=tr.matmul([tr.translate(-1.5*i,0,0),stretch.transform])
            roadsV.childs+=[stretch]
    roads.childs+=[roadsV]
    #En sentido "horizontal"
    roadsH = sg.SceneGraphNode('roadH')
    stretch=createEnvNode("stretch lower",gpuRoad,"H",9,"Road")
    stretch.transform=tr.matmul([tr.translate(-1.5*8,0,-1.5),stretch.transform])
    roadsH.childs+=[stretch]
    stretch=createEnvNode("stretch upper",gpuRoad,"H",7,"Road")
    stretch.transform=tr.matmul([tr.translate(-1.5*8,0,1.5*13),stretch.transform])
    roadsH.childs+=[stretch]
    roads.childs+=[roadsH]
    gpuRoad2=setupGpu(pipeline,"pista.jpg",2)
    curvedRoads=sg.SceneGraphNode("curvedRoads")
    #Las esquinas de las curvas
    curve=createEnvNode("curve1",gpuRoad2,"C",1,"Road")
    curve.transform=tr.matmul([tr.translate(1.5-0.135,0,14.66445),tr.shearing(0,0,-0.306,0.0055),curve.transform])
    curve2=createEnvNode("curve2",gpuRoad2,"C",1,"Road")
    curve2.transform=tr.matmul([tr.translate(-1.89,0,19.35),tr.shearing(0,0,-0.285,0.00055),tr.scale(0.81,1,1.05),tr.rotationY(-np.pi/2+np.deg2rad(20)),tr.rotationX(np.pi),curve2.transform])
    curve3=createEnvNode("curve3",gpuRoad2,"C",1,"Road")
    curve3.transform=tr.matmul([tr.translate(-1.621,0,19.15),tr.rotationY(np.deg2rad(9.75)),tr.shearing(0,0,-0.37,0.0055),tr.rotationY(-np.pi/2+np.deg2rad(37)),tr.scale(1.1377,1,0.687),tr.rotationX(-np.pi),curve3.transform])
    curvedRoads.childs+=[curve3]
    curvedRoads.childs+=[curve2]
    curvedRoads.childs+=[curve]
    roads.childs+=[curvedRoads]
    #La parte "diagonal" de la pista (el límite izquierdo superior de la escena visto desde arriba)
    diagonalRoads=sg.SceneGraphNode("diagonalRoads")
    stretch=createEnvNode("stretch " + str(i),gpuRoad,"H",3,"Road")
    #La inclinación está dada por la pendiente de la hipotenusa del triángulo que contiene el pasto
    stretch.transform=tr.matmul([tr.translate(-1.12,0,18.41),tr.rotationY(np.arctan(4.5/3)),tr.scale(1.2,1,1),stretch.transform])
    diagonalRoads.childs+=[stretch]
    roads.childs+=[diagonalRoads]
    environment.childs+=[roads]

    return scene

#Esta función crea un nodo de grafo de escena que representa al sol y la luna, debe ser aparte porque usan
#un shader/pipeline distinto
def createSatellites(pipeline):
    gpuSun=setupOBJ(pipeline,"sun.obj",(1.,1.,51/255.))
    gpuMoon=setupOBJ(pipeline,"moon.obj",(229/255.,216/255.,152/255.))
    satellites=sg.SceneGraphNode("Satellites")
    sun=createSatelliteNode("Sun",gpuSun,"Sun")
    moon=createSatelliteNode("Moon",gpuMoon,"Moon")
    satellites.childs+=[sun]
    satellites.childs+=[moon]
    return satellites

#Función para crear los postes de luz
def createLampScene(pipeline):
    #Nodo raíz de las luces
    lamps=sg.SceneGraphNode("lamps")
    #Nodos para el primer grupo de casas separado en 2 grupos
    lampGroup1=sg.SceneGraphNode("lampGroup1")
    lampGroup2=sg.SceneGraphNode("lampGroup2")
    #Se crea el gpuShape usado a lo largo de toda la función
    gpuLamp=setupOBJ(pipeline,getAssetPath("lampPost.obj"),(0.5,0.5,0.5))
    for j in range(0,10,2):
        node=createLamp("lamp "+str(j),gpuLamp,0,1.5*j)
        lampGroup1.childs+=[node]
        node=createLamp("lamp "+str(j),gpuLamp,-1.5,1.5*j)
        lampGroup2.childs+=[node]
    #Cada fila de postes debe tener una correción respecto a las casas
    #Y además deben apuntar hacia "afuera" (a la calle)
    lampGroup1.transform=tr.translate(0.5,0,0)
    lampGroup2.transform=tr.translate(-0.5,0,0)
    #Nodos para el segundo grupo de casas
    lampGroup3=sg.SceneGraphNode("lampGroup3")
    lampGroup4=sg.SceneGraphNode("lampGroup4")
    for j in range(0,13,2):
        node=createLamp("lamp "+str(j),gpuLamp,-1.5*3,1.5*j)
        lampGroup3.childs+=[node]
        node=createLamp("lamp "+str(j),gpuLamp,-1.5*4,1.5*j)
        lampGroup4.childs+=[node]
    lampGroup3.transform=tr.translate(0.5,0,0)
    lampGroup4.transform=tr.translate(-0.5,0,0)
    #Para el tercer grupo
    lampGroup5=sg.SceneGraphNode("lampGroup5")
    lampGroup6=sg.SceneGraphNode("lampGroup6")
    for i in range(6,8):
        for j in range(0,13,2):
            node=createLamp("lamp "+str(j),gpuLamp,-1.5*6,1.5*j)
            lampGroup5.childs+=[node]
            node=createLamp("lamp "+str(j),gpuLamp,-1.5*7,1.5*j)
            lampGroup6.childs+=[node]
    lampGroup5.transform=tr.translate(0.5,0,0)
    lampGroup6.transform=tr.translate(-0.5,0,0)
    #Se añaden al nodo raíz
    lamps.childs+=[lampGroup1]
    lamps.childs+=[lampGroup2]
    lamps.childs+=[lampGroup3]
    lamps.childs+=[lampGroup4]
    lamps.childs+=[lampGroup5]
    lamps.childs+=[lampGroup6]
    #Se desplazan todos los postes un poco respecto a las casas (para no tapar las puertas)
    lamps.transform=tr.translate(0,0,-0.65)
    return lamps


#Función general para formar un gpuShape
def setupGpu(pipeline,imgName,param=0):
    #Se separa el nombre del archivo antes y después del punto, esto para
    #descartar la extensión al determinar que textura es y hacer el shape apropiado
    fullName=imgName.split('.')
    name=fullName[0]
    #Si tiene un numero al final, descartarlo (mantener todo menos el último caracter), si no, no hacer nada
    name=name[:-1] if name[-1].isnumeric() else name
    #Dependiendo de textura se entregó, se crea el shape que corresponde
    if (name=="ladrillo" or name=="piso" or name=="pista") and param==0:
        shape = bs.createTextureCubeWithNormals()
    elif name=="tejado" or param==3:
        shape = bs.createTexturePyramidWithNormals()
    elif name=="pasto" or param==2:
        shape = bs.createGrassWithNormals()
    elif name=="ventana":
        shape= bs.createWindow2WithNormals() if imgName=="ventana2.png" else bs.createWindow1WithNormals()
    elif name=="puerta":
        shape = bs.createDoor1WithNormals() if imgName=="puerta1.jpg" else bs.createDoor2WithNormals()
    else:
        shape= bs.createTextureCilinderWithNormals(15,15)
    #Se carga en el shader
    gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu)
    gpu.fillBuffers(
        shape.vertices, shape.indices)
    gpu.texture = es.textureSimpleSetup(
        getAssetPath(imgName), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    return gpu

#Función para leer un archivo obj y retornar su gpuShape
def setupOBJ(pipeline,filename,color):
    shape=readOBJ(getAssetPath(filename),color)
    gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu)
    gpu.fillBuffers(
        shape.vertices, shape.indices)
    return gpu
    

#Función auxiliar para el techo que no es una pirámide
def setupRoof2(pipeline,imgName):
    shapeRoof = bs.createTextureTrapezoidWithNormals()
    gpuRoof = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRoof)
    gpuRoof.fillBuffers(
        shapeRoof.vertices, shapeRoof.indices)
    gpuRoof.texture = es.textureSimpleSetup(
        getAssetPath(imgName), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    return gpuRoof

#Función para crear una casa completa dada sus gpuShape, su posición y su "tipo"
#Donde el tipo determina la forma que tiene la casa
def createHouseNode(name,gpuList,posX,posZ,t):
    #Nodo principal de esta casa, estara desplazado según posX y posZ
    nodoCasa = sg.SceneGraphNode(name)
    nodoCasa.transform=tr.translate(posX,0.0965,posZ)
    #Paredes
    wall=gpuList[0]
    nodoParedes=sg.SceneGraphNode(name + " walls")
    nodoParedes.childs+=[wall]
    nodoParedes.transform=tr.matmul([tr.translate(0,0.2,0),tr.scale(0.5,0.5,1)])
    nodoCasa.childs+=[nodoParedes]
    roof=gpuList[1]
    roof2=gpuList[4]
    #Techo
    nodoTecho=sg.SceneGraphNode(name + " roof")
    nodoTecho.childs+=[roof]
    if t==1:
        #Si es casa tipo 1, es de 1 piso
        nodoTecho.transform=tr.matmul([tr.translate(0,0.65,0),tr.scale(0.75,0.45,1.3)])
    nodoCasa.childs+=[nodoTecho]
    door=gpuList[2]
    #Puerta, separada en 2 nodos por el marco y la chapa
    nodoPuerta=sg.SceneGraphNode(name + " door")
    nodoMarco=sg.SceneGraphNode(name + " frame")
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
    #Ventanas
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
    #Si es casa de tipo 2
    if t==2:
        #Segundo piso
        nodoSegundoPiso=sg.SceneGraphNode(name + " second floor")
        nodoSegundoPiso.childs+=[wall]
        nodoSegundoPiso.transform=tr.matmul([tr.translate(0,0.7005,0),tr.scale(0.5,0.5,0.8)])
        nodoCasa.childs+=[nodoSegundoPiso]
        #Reubicación de techo
        nodoTecho.transform=tr.matmul([tr.translate(0,1.09,0),tr.scale(0.75,0.45,1)])
        #Otros techos
        nodoTecho2=sg.SceneGraphNode(name + " second roof")
        nodoTecho2.childs+=[roof2]
        nodoTecho2.transform=tr.matmul([tr.translate(0,0.55,0.5),tr.scale(0.6,0.2,0.2)])
        nodoCasa.childs+=[nodoTecho2]
        nodoTecho3=sg.SceneGraphNode(name + " third roof")
        nodoTecho3.childs+=[roof2]
        nodoTecho3.transform=tr.matmul([tr.translate(0,0.55,-0.5),tr.rotationY(np.pi),tr.scale(0.6,0.2,0.2)])
        nodoCasa.childs+=[nodoTecho3]
        #Más ventanas
        nodoVentana4=sg.SceneGraphNode(name + " window4")
        nodoVentana4.childs+=[window]
        nodoVentana4.transform=tr.matmul([tr.translate(0.25,0.7,0),tr.rotationY(-np.pi/2),tr.scale(0.33,0.22,0.04)])
        nodoCasa.childs+=[nodoVentana4]
        nodoVentana5=sg.SceneGraphNode(name + " window5")
        nodoVentana5.childs+=[window]
        nodoVentana5.transform=tr.matmul([tr.translate(-0.25,0.7,0),tr.rotationY(-np.pi/2),tr.scale(0.33,0.22,0.04)])
        nodoCasa.childs+=[nodoVentana5]
    #Si es casa de tipo 3
    elif t==3:
        #Es de tamaño ligeramente diferente
        nodoParedes.transform=tr.matmul([tr.translate(-0.15,0.2,0),tr.scale(0.8,0.5,1)])
        #Segundo piso
        nodoSegundoPiso=sg.SceneGraphNode(name + " second floor")
        nodoSegundoPiso.childs+=[wall]
        nodoSegundoPiso.transform=tr.matmul([tr.translate(-0.325,0.65,0),tr.scale(0.45,0.4,1)])
        nodoCasa.childs+=[nodoSegundoPiso]
        #Reubicación de techo y ventanas
        nodoTecho.transform=tr.matmul([tr.translate(-0.35,1.05,0),tr.scale(0.75,0.45,1.2)])
        nodoVentana1.transform=tr.matmul([tr.translate(-0.55,0.25,0),tr.rotationY(-np.pi/2),tr.scale(0.33,0.22,0.04)])
        nodoVentana2.transform=tr.matmul([tr.translate(-0.15,0.25,-0.49),tr.scale(0.33,0.22,0.04)])
        nodoVentana3.transform=tr.matmul([tr.translate(-0.15,0.25,0.49),tr.scale(0.33,0.22,0.04)])
        nodoVentana4=sg.SceneGraphNode(name + " window4")
        nodoVentana4.childs+=[window]
        nodoVentana4.transform=tr.matmul([tr.translate(-0.1,0.63,0),tr.rotationY(-np.pi/2),tr.scale(0.66,0.35,0.04)])
        nodoCasa.childs+=[nodoVentana4]
        nodoVentana5=sg.SceneGraphNode(name + " window5")
        nodoVentana5.childs+=[window]
        nodoVentana5.transform=tr.matmul([tr.translate(-0.55,0.7,0),tr.rotationY(-np.pi/2),tr.scale(0.33,0.22,0.04)])
        nodoCasa.childs+=[nodoVentana5]
    #Según la posición espacial de la casa en la escena, esta debe o no estar rotada para "mirar hacia la calle"
    if int((posX/-1.5))%2==0:
        if posX>=-6 and posX<=-1:
            nodoCasa.transform=tr.matmul([tr.translate(posX,0.0965,posZ),tr.rotationY(np.pi)])
    elif int((posX/-1.5))%2==1: 
        if posX>=-2.2 or posX<=-8:
            nodoCasa.transform=tr.matmul([tr.translate(posX,0.0965,posZ),tr.rotationY(np.pi)])

    return nodoCasa

#Función para crear un nodo del entorno, ya sea piso, pista o pasto
def createEnvNode(name,gpu,direction,length,type="Floor"):
    #Nodo principal
    nodoEntorno=sg.SceneGraphNode(name)
    #Si es parte de una curva o es el pasto
    if direction=="C":
        nodoCuadro=sg.SceneGraphNode(name + " tile")
        if type=="Road":
            nodoCuadro.transform=tr.matmul([tr.scale(1.52,0.1005,0.8425),tr.rotationY(-np.pi/2),tr.rotationZ(np.pi)])
        elif type=="Pasto":
            nodoCuadro.transform=tr.matmul([tr.translate(0,0.07,0),tr.rotationZ(np.pi),tr.scale(3,0.025,4.5)])
        else:
            nodoCuadro.transform=tr.matmul([tr.rotationZ(np.pi),tr.scale(3,0.1,4.5)])
        nodoCuadro.childs+=[gpu]
        nodoEntorno.childs+=[nodoCuadro]
    #Si no
    else:
        for i in range(length):
            nodoCuadro=sg.SceneGraphNode(name + " tile " + str(i))
            nodoCuadro.transform=tr.matmul([tr.scale(1.5,0.1,1.5)])
            #Si es "vertical"
            if direction=="V":
                if type=="Road":
                    nodoCuadro.transform=tr.matmul([tr.translate(0,0,1.5*i),tr.rotationY(np.pi/2),nodoCuadro.transform])
                else:
                    nodoCuadro.transform=tr.matmul([tr.translate(0,0,1.5*i),nodoCuadro.transform])
            else:
                nodoCuadro.transform=tr.matmul([tr.translate(1.5*i,0,0),nodoCuadro.transform])
            nodoCuadro.childs+=[gpu]
            nodoEntorno.childs+=[nodoCuadro]
    return nodoEntorno

#Función para crear un nodo satelite, ya sea el sol o la luna
def createSatelliteNode(name,gpu,type):
    nodoSatelite=sg.SceneGraphNode(name)
    nodoSatelite.childs+=[gpu]
    #El sol y la luna tienen la misma posición x,z pero opuestos en y según el origen
    nodoSatelite.transform=tr.matmul([tr.translate(-6,30,7),tr.scale(0.02,0.025,0.02)])
    if type=="Moon":
        nodoSatelite.transform=tr.matmul([tr.translate(-6,-30,7),tr.scale(0.02,0.02,0.02)])
    return nodoSatelite

#Función para crear un nodo poste de luz
def createLamp(name,gpu,posX,posZ):
    nodoPoste=sg.SceneGraphNode(name)
    nodoPoste.childs+=[gpu]
    #Al exportar el obj de blender me quedó acostado, por eso la rotación en X para enderezar
    #es bastante grande también
    nodoPoste.transform=tr.matmul([tr.translate(posX,0.7,posZ),tr.scale(0.1,0.13,0.1),tr.rotationX(np.pi/2)])
    if int((posX/-1.5))%2==0:
        if posX>=-6 and posX<=-1:
            nodoPoste.transform=tr.matmul([tr.translate(posX,0.7,posZ),tr.scale(0.1,0.13,0.1),tr.rotationY(np.pi),tr.rotationX(np.pi/2)])
    elif int((posX/-1.5))%2==1: 
        if posX>=-2.2 or posX<=-8:
            nodoPoste.transform=tr.matmul([tr.translate(posX,0.7,posZ),tr.scale(0.1,0.13,0.1),tr.rotationY(np.pi),tr.rotationX(np.pi/2)])
    return nodoPoste

#Función para crear el nodo con el auto
def createCar(pipeline):
    #Nodo raíz
    car=sg.SceneGraphNode("Car")
    #Nodo para el cuerpo
    body=sg.SceneGraphNode("body")
    #Gpu shape del cuerpo
    gpuBody=setupOBJ(pipeline,"car.obj",(233/255.,203/255.,70/255.))
    body.childs+=[gpuBody]
    #Gpu shape de las ruedas
    gpuWheel=setupOBJ(pipeline,"wheel.obj",(0.,0.,0.))
    #Nodo para contener todas las ruedas
    wheels=sg.SceneGraphNode("Wheels")
    #Ruedas frontales
    front=sg.SceneGraphNode("FrontWheels")
    #Ruedas traseras
    back=sg.SceneGraphNode("BackWheels")
    #Nodos frontales derecho e izquierdo
    frontR=sg.SceneGraphNode("FrontRight")
    frontR.childs+=[gpuWheel]
    frontR.transform=tr.translate(-1.1,0,1.7)
    frontL=sg.SceneGraphNode("FrontLeft")
    frontL.childs+=[gpuWheel]
    frontL.transform=tr.translate(0.9,0,1.7)
    #Nodos traseros
    backR=sg.SceneGraphNode("BackRight")
    backR.childs+=[gpuWheel]
    backR.transform=tr.translate(-1.1,0,-1.4)
    backL=sg.SceneGraphNode("BackLeft")
    backL.childs+=[gpuWheel]
    backL.transform=tr.translate(0.9,0,-1.4)
    front.transform=tr.translate(0,-0.35,0)
    front.childs+=[frontR,frontL]
    back.transform=tr.translate(0,-0.35,0)
    back.childs+=[backR,backL]
    wheels.childs+=[front,back]
    car.childs+=[body,wheels]
    car.transform=tr.matmul([tr.rotationY(-np.pi/2),tr.scale(0.2,0.2,0.2)])
    return (car,frontR,backR,frontL,backL)