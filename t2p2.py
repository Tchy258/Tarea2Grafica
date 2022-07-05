from re import A
import glfw
from OpenGL.GL import *
from grafica.setup import setProjection, setView, createScene,createSatellites,createLampScene
from grafica.gpu_shape import GPUShape
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import numpy as np
import grafica.transformations as tr
import grafica.scene_graph as sg
import grafica.constants as constants
from grafica.controller import Controller,Spotlight
import math

#Objeto para controlar la camara
controller=Controller()
#Diccionario de luces
spotlightsPool = dict()

def setLights():
    #Luz de la linterna
    spot1 = Spotlight()
    spot1.ambient = np.array([0.5, 0.5, 0.5])
    spot1.diffuse = np.array([1.0, 1.0, 1.0])
    spot1.specular = np.array([1.0, 1.0, 1.0])
    spot1.constant = 1.0
    spot1.linear = 0.09
    spot1.quadratic = 0.032
    spot1.position = controller.camPos #Sigue a la cámara
    spot1.direction = controller.camFront #Apunta donde mire la camara
    spot1.cutOff = np.cos(np.radians(12.5)) #Como es una linterna, el ángulo es pequeño
    spot1.outerCutOff = np.cos(np.radians(30)) 
    spotlightsPool['spot1'] = spot1 #Se guarda en el dicionario de luces

    baseString='spot'
    for i in range(2,40):
        spot=Spotlight()
        spot.ambient = np.array([0.0, 0.0, 0.0])
        spot.diffuse = np.array([0.6, 0.6, 0.6])
        spot.specular = np.array([0.6, 0.6, 0.6])
        spot.constant = 0.9
        spot.linear = 0.3
        spot.quadratic = 0.06
        spot.position = np.array([0,0,0]) 
        spot.direction = np.array([0,-1,0]) #Apunta donde mire la camara
        spot.cutOff = np.cos(np.radians(12.5)) #Como es una linterna, el ángulo es pequeño
        spot.outerCutOff = np.cos(np.radians(45))
        spotlightsPool[baseString+str(i)] = spot
    k=1
    for j in range(0,10,2):
        k+=1
        spot = spotlightsPool[baseString+str(k)]
        spot.position = np.array([-1.5-0.8,1.46,1.5*j-0.65])
        k+=1
        spot = spotlightsPool[baseString+str(k)]
        spot.position = np.array([0+0.8,1.46,1.5*j-0.65])
    for j in range(0,13,2):
        k+=1
        spot = spotlightsPool[baseString+str(k)]
        spot.position = np.array([-(1.5*3)+0.8,1.46,1.5*j-0.65])
        k+=1
        spot = spotlightsPool[baseString+str(k)]
        spot.position = np.array([-(1.5*4)-0.8,1.46,1.5*j-0.65])
        k+=1
        spot = spotlightsPool[baseString+str(k)]
        spot.position = np.array([-(1.5*6)+0.8,1.46,1.5*j-0.65])
        k+=1
        spot = spotlightsPool[baseString+str(k)]
        spot.position = np.array([-(1.5*7)-0.8,1.46,1.5*j-0.65])



#Funcion para manejar el movimiento del mouse
def cursor_pos_callback(window,x,y):
    global controller
    #offsetX y offsetY muestran que tanto se ha movido el mouse desde el ultimo swap de buffers
    offsetX=x - controller.mouseX
    offsetY=controller.mouseY - y
    #x e y son las nuevas coordenadas actuales del mouse
    controller.mouseX=x
    controller.mouseY=y
    if not controller.IsOrtho and controller.cursorShouldHide:
        #Los offset se multiplican para tener un movimiento que no sea extremedamente brusco
        sensitivity=0.2
        offsetX*=sensitivity
        offsetY*=sensitivity
        #El angulo phi de la camara se mueve segun el offsetX en radianes
        controller.cameraPhiAngle+=np.deg2rad(offsetX)
        #Si no se ha movido el mouse en x, y la variable del angulo phi es mayor a 2pi
        if (abs(controller.cameraPhiAngle)>=2*np.pi and offsetX==0):
            #Se suma o resta 2pi segun corresponda para evitar algun posible overflow de la variable al dar
            #una cantidad muy grande de vueltas con el mouse
            controller.cameraPhiAngle= controller.cameraPhiAngle-2*np.pi if controller.cameraPhiAngle > 0 \
                                        else controller.cameraPhiAngle + 2*np.pi
    
        #Si el angulo theta esta entre -pi/2 y pi/2
        if (abs(controller.cameraThetaAngle)<np.pi/2):
            controller.cameraThetaAngle+=np.deg2rad(offsetY)
            if(controller.cameraThetaAngle>=np.pi/2):
                controller.cameraThetaAngle=np.pi/2-np.pi/(2*constants.SCREEN_HEIGHT)
            if(controller.cameraThetaAngle<=-np.pi/2):
                controller.cameraThetaAngle=-np.pi/2+np.pi/(2*constants.SCREEN_HEIGHT)
    
        frontX=np.cos(controller.cameraPhiAngle)*np.cos(controller.cameraThetaAngle)
        frontZ=np.sin(controller.cameraPhiAngle)*np.cos(controller.cameraThetaAngle)
        frontY=np.sin(controller.cameraThetaAngle)
        controller.camFront=np.array([frontX,frontY,frontZ])
        controller.camFront/=np.linalg.norm(controller.camFront)

#Funcion para registrar clicks y botones del mouse
def mouse_button_callback(window,button,action,mods):
    global controller
    #Al hacer click izquierdo se mantiene o suelta el mouse en la ventana
    if (button==glfw.MOUSE_BUTTON_1 and action==glfw.PRESS):
        if (controller.cursorShouldHide):
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
            controller.cursorShouldHide=False
        else:
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
            controller.cursorShouldHide=True
    #Al hacer click derecho se prende o apaga la linterna
    if (button==glfw.MOUSE_BUTTON_2 and action==glfw.PRESS):
        controller.flashlightOn=not controller.flashlightOn

#Funciones para teclas
def on_key(window, key, scancode, action, mods):


    global controller
    
    if key==glfw.KEY_SPACE and action==glfw.PRESS:
        controller.IsOrtho=not controller.IsOrtho
    if key==glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

def check_key_inputs(window):
    if not controller.IsOrtho:
        #Con shift se va más rápido
        if glfw.get_key(window, glfw.KEY_LEFT_SHIFT)==glfw.PRESS or glfw.get_key(window, glfw.KEY_LEFT_SHIFT)==glfw.REPEAT:
            controller.camSpeed*=4
        #WASD para moverse, W y S solo suman o restan su producto con el vector look at de la camara
        if glfw.get_key(window, glfw.KEY_W)==glfw.PRESS or glfw.get_key(window, glfw.KEY_W)==glfw.REPEAT:
            controller.camPos+=controller.camFront*controller.camSpeed
        if glfw.get_key(window, glfw.KEY_S)==glfw.PRESS or glfw.get_key(window, glfw.KEY_S)==glfw.REPEAT:
            controller.camPos-=controller.camFront*controller.camSpeed
        #A y D usan un producto cruz para calcular que es derecha y que es izquierda para la vista actual
        if glfw.get_key(window, glfw.KEY_A)==glfw.PRESS or glfw.get_key(window, glfw.KEY_A)==glfw.REPEAT:
            sidewayVector=np.cross(controller.camFront,controller.camUp)
            #Estos vectores se normalizan para no ir más rápido solo cuando se mira a cierta dirección
            sidewayVector/=np.linalg.norm(sidewayVector)
            controller.camPos-=(sidewayVector*controller.camSpeed)
        if glfw.get_key(window, glfw.KEY_D)==glfw.PRESS or glfw.get_key(window, glfw.KEY_D)==glfw.REPEAT:
            sidewayVector=np.cross(controller.camFront,controller.camUp)
            sidewayVector/=np.linalg.norm(sidewayVector)
            controller.camPos+=(sidewayVector*controller.camSpeed)
        #Limites de la escena, este primer if es la función de la recta que delimita la línea diagonal
        #del pentagono, en la pista al lado del pasto
        # if controller.camPos[2]>-1.44245*controller.camPos[0] + 29.31872:
        #     controller.camPos[2]=-1.44245*controller.camPos[0] + 29.31872
        #     controller.camPos[0]=controller.camPos[2]/-1.44245 - 29.31872/-1.44245
        #if controller.camPos[0]>2.2:
        #    controller.camPos[0]=2.2
        #if controller.camPos[0]<-12.6:
        #    controller.camPos[0]=-12.6
        #if controller.camPos[1]>6:
        #    controller.camPos[1]=6
        #if controller.camPos[1]<0.2:
        #    controller.camPos[1]=0.2
        #if controller.camPos[2]>19.5:
        #    controller.camPos[2]=19.5
        #if controller.camPos[2]<-2:
        #    controller.camPos[2]=-2
        #La linterna se mueve junto con la cámara
        spotlightsPool['spot1'].position=controller.camPos
        spotlightsPool['spot1'].direction=controller.camFront
        
#Esta función imprime la hora cuando ha pasado 1 hora del día
#una hora está definida arbitrariamiente como un desplace de 15 grados
#del sol o la luna
def timeOfDay(theta,anterior):
    anguloEnGrados=np.rad2deg(theta)
    horas=((math.ceil(anguloEnGrados)//15)+12)%24
    if abs(horas-anterior)==1 or abs(math.ceil(anguloEnGrados)-180)<1:
        if horas<10:
            print("0"+str(horas)+":00")
        else:
            print(str(horas)+":00")
    return horas

#Esta función toma un valor de temperatura de color en Kelvin y la convierte a
#RGB, fue adaptada de https://tannerhelland.com/2012/09/18/convert-temperature-rgb-algorithm-code.html
def temperatureToRGB(temp,rojo,verde,azul):
    if temp<=66:
        r = 255.
        g = temp
        g = 99.4708025861 * math.log(g) - 161.1195681661
        if g < 0:
            g=0
        if g > 255:
            g=255
        if temp<=19:
            b=0
        else:
            b=temp-10
            b=138.5177312231 * math.log(b) - 305.0447927307
            if b < 0:
                b=0
            if b > 255:
                b=255
    else:
        b=255.
        r=temp-60
        g=temp-60
        r=329.698727446*(r**(-0.1332047592))
        g=288.1221695283 * (g**(-0.0755148492))
        if r < 0:
            r = 0
        if r > 255:
            r = 255
        if g < 0:
            g=0
        if g > 255:
            g=255
    return ((abs(r/255.-rojo)),abs(g/255.-verde),abs(b/255.-azul))

def main():
    #Si no se pudo iniciar glfw, se cierra la ventana
    if not glfw.init():
        glfw.set_window_should_close(window,True)
    
    #Se instancia la ventana
    window=glfw.create_window(constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT,constants.TITLE,None,None)
    
    #Si no se pudo crear la ventana
    if not window:
        #Se termina glfw y se cierra la ventana
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    #Se dibuja en la ventana de window
    glfw.make_context_current(window)

    #Función on_key para capturar entrada de teclado
    glfw.set_key_callback(window, on_key)

    #Shaders de texturas y shader de camera respectivamente
    textureShaderProgram = ls.MultipleLightTexturePhongShaderProgram()
    colorShaderProgram = ls.MultipleLightPhongShaderProgram()
    grafoEscena=createScene(textureShaderProgram)
    satelites=createSatellites(colorShaderProgram)
    postes=createLampScene(colorShaderProgram)
    luna=sg.findNode(satelites,"Moon")
    #Color del fondo
    temperatura=3000
    (rojoCielo,verdeCielo,azulCielo)=temperatureToRGB(temperatura,0,0,0)
    glClearColor(rojoCielo, verdeCielo, azulCielo, 0.5)
    #Testeo de profundidad para mostrar correctamente objetos 3D
    glEnable(GL_DEPTH_TEST)
    setLights()
    #Para que el mouse se quede dentro de la ventana y se pueda mover la camara libremente
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    #Para que la ventana registre los clicks del mouse
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    #Para registrar la posición del mouse
    glfw.set_cursor_pos_callback(window,cursor_pos_callback)
    #Calculos de tiempo para el movimiento de la cámara
    t0 = glfw.get_time()
    t1 = t0
    rotacionSatelites=0
    rotacionLuna=0
    horaAnterior=11
    estaAnocheciendo=True
    deltaRojo=0
    deltaVerde=0
    deltaAzul=0
    rojoAtardecer=0
    verdeAtardecer=0
    azulAtardecer=0
    rojoNoche=0
    verdeNoche=0
    azulNoche=0
    while not glfw.window_should_close(window):
        t1=glfw.get_time()
        dt=t1-t0
        t0=t1
        #La velocidad actual será la velocidad base multiplicada por dt
        controller.camSpeed=controller.camBaseSpeed*dt
        rotacionLuna+=(np.pi/128)*dt
        rotacionSatelites+=(np.pi/31)*dt
        if abs(rotacionSatelites)>2*np.pi:
            rotacionSatelites-=2*np.pi
        if abs(rotacionLuna)>2*np.pi:
            rotacionLuna-=2*np.pi
        luna.transform=tr.matmul([luna.transform,tr.rotationY(rotacionLuna)])
        satelites.transform=tr.rotationZ(rotacionSatelites)
        horaAnterior=timeOfDay(rotacionSatelites,horaAnterior)
        if horaAnterior>16 or horaAnterior<2:
            estaAnocheciendo=True
        else:
            estaAnocheciendo=False
        print(controller.camPos)
        glfw.poll_events()
        check_key_inputs(window)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #Se cambian la vista y proyección de ser necesario
        setView(textureShaderProgram,colorShaderProgram,controller)
        setProjection(controller, textureShaderProgram,colorShaderProgram,constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT,spotlightsPool,rotacionSatelites,horaAnterior)

        glUseProgram(textureShaderProgram.shaderProgram)
        #Se dibuja la escena
        sg.drawSceneGraphNode(grafoEscena, textureShaderProgram, "model")
        glUseProgram(colorShaderProgram.shaderProgram)
        sg.drawSceneGraphNode(satelites, colorShaderProgram, "model")
        glUseProgram(colorShaderProgram.shaderProgram)
        sg.drawSceneGraphNode(postes,colorShaderProgram,"model")
        (deltaRojo,deltaVerde,deltaAzul)=temperatureToRGB(temperatura,rojoCielo,verdeCielo,azulCielo)
        if estaAnocheciendo:
            temperatura-= 100*dt*(1-abs(np.cos(rotacionSatelites)))
            if temperatura<=1:
                temperatura=1
            rojoCielo-=deltaRojo*dt
            verdeCielo-=deltaVerde*dt
            azulCielo-=deltaAzul*dt
        else:
            temperatura+= 500*dt*(1-abs(np.cos(rotacionSatelites)))
            if temperatura>=3000:
                temperatura=3000
            rojoCielo+=deltaRojo*dt
            verdeCielo+=deltaVerde*dt
            azulCielo+=deltaAzul*dt
        if temperatura<1: temperatura+=10
        if (horaAnterior>=17 and horaAnterior<=19) or (horaAnterior>=4 and horaAnterior<=5):
            rojoAtardecer=(rojoCielo+1/255.)*10
            verdeAtardecer=verdeCielo
            azulAtardecer=(azulCielo+1/255.)/10
            glClearColor(rojoAtardecer, verdeAtardecer, azulAtardecer, 0.5)
        else:
            if (horaAnterior>=20 and horaAnterior<=23) or (horaAnterior>=0 and horaAnterior<=2):
                rojoNoche=rojoCielo/10
                verdeNoche=verdeCielo/10
                azulNoche=azulCielo/5
                glClearColor(rojoNoche, verdeNoche, azulNoche, 0.5)
            else:
                glClearColor(rojoCielo, verdeCielo, azulCielo, 0.5)
        glfw.swap_buffers(window)
    
    grafoEscena.clear()
    satelites.clear()
if __name__ == "__main__":

    main()