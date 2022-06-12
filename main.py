import glfw
from OpenGL.GL import *
from setup import setProjection, setView, createScene
from gpu_shape import GPUShape
import basic_shapes as bs
import easy_shaders as es
import numpy as np
import transformations as tr
import scene_graph as sg
import constants
import math
import random
from controller import Controller

controller=Controller()

#Funcion para manejar el movimiento del mouse
def cursor_pos_callback(window,x,y):
    global controller
    #offsetX y offsetY muestran que tanto se ha movido el mouse desde el ultimo swap de buffers
    offsetX=x - controller.mouseX
    offsetY=controller.mouseY - y
    #x e y son las nuevas coordenadas actuales del mouse
    controller.mouseX=x
    controller.mouseY=y
    if not controller.IsOrtho:
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
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
            controller.cursorShouldHide=False
        else:
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)

#Funcion para detectar si el mouse entró o salió de la ventana)
def cursor_enter_callback(window,entered):
    global controller

    if entered:
        controller.cursorShouldHide=True
    else:
        controller.cursorShouldHide=False

def on_key(window, key, scancode, action, mods):


    global controller
    
    if key==glfw.KEY_SPACE and action==glfw.PRESS:
        controller.IsOrtho=not controller.IsOrtho
    if key==glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

def check_key_inputs(window):
    if not controller.IsOrtho:
        if glfw.get_key(window, glfw.KEY_LEFT_SHIFT)==glfw.PRESS or glfw.get_key(window, glfw.KEY_LEFT_SHIFT)==glfw.REPEAT:
            controller.camSpeed*=4
        if glfw.get_key(window, glfw.KEY_W)==glfw.PRESS or glfw.get_key(window, glfw.KEY_W)==glfw.REPEAT:
            controller.camPos+=controller.camFront*controller.camSpeed
        if glfw.get_key(window, glfw.KEY_S)==glfw.PRESS or glfw.get_key(window, glfw.KEY_S)==glfw.REPEAT:
            controller.camPos-=controller.camFront*controller.camSpeed
        if glfw.get_key(window, glfw.KEY_A)==glfw.PRESS or glfw.get_key(window, glfw.KEY_A)==glfw.REPEAT:
            sidewayVector=np.cross(controller.camFront,controller.camUp)
            sidewayVector/=np.linalg.norm(sidewayVector)
            controller.camPos-=(sidewayVector*controller.camSpeed)
        if glfw.get_key(window, glfw.KEY_D)==glfw.PRESS or glfw.get_key(window, glfw.KEY_D)==glfw.REPEAT:
            sidewayVector=np.cross(controller.camFront,controller.camUp)
            sidewayVector/=np.linalg.norm(sidewayVector)
            controller.camPos+=(sidewayVector*controller.camSpeed)
        if controller.camPos[0]>2.25:
            controller.camPos[0]=2.25
        if controller.camPos[0]<-7.5:
            controller.camPos[0]=-7.5
        if controller.camPos[1]>4:
            controller.camPos[1]=4
        if controller.camPos[1]<0.2:
            controller.camPos[1]=0.2
        if controller.camPos[2]>2.25:
            controller.camPos[2]=2.25
        if controller.camPos[2]<-6.5:
            controller.camPos[2]=-6.5


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
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()
    grafoEscena=createScene(textureShaderProgram)
    #Color del fondo
    glClearColor(0.85, 0.85, 0.85, 1.0)

    #Testeo de profundidad para mostrar correctamente objetos 3D
    glEnable(GL_DEPTH_TEST)

    #Para que el mouse se quede dentro de la ventana y se pueda mover la camara libremente
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    #Para que la ventana registre los clicks del mouse
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    glfw.set_cursor_enter_callback(window, cursor_enter_callback)
    glfw.set_cursor_pos_callback(window,cursor_pos_callback)
    t0 = glfw.get_time()
    t1 = t0
    while not glfw.window_should_close(window):
        t1=glfw.get_time()
        dt=t1-t0
        t0=t1
        controller.camSpeed=controller.camBaseSpeed*dt
        glfw.poll_events()
        check_key_inputs(window)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        print(controller.camPos)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        setView(textureShaderProgram,colorShaderProgram,controller)
        setProjection(controller, textureShaderProgram,colorShaderProgram,constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT)

        glUseProgram(textureShaderProgram.shaderProgram)
        sg.drawSceneGraphNode(grafoEscena, textureShaderProgram, "model")

        glfw.swap_buffers(window)
    
    grafoEscena.clear()
    
if __name__ == "__main__":

    main()