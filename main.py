import glfw
from OpenGL.GL import *
from gpu_shape import GPUShape
import basic_shapes as bs
import easy_shaders as es
import numpy as np
import transformations as tr
import constants
import math
import random

#Clase para manejar la camara y movimiento
class Controller:
    def __init__(self):
        self.cameraPhiAngle = 0
        self.cameraThetaAngle = 0
        self.camSpeed= 0.5
        self.camPos=np.array([0.,0.,0.])
        self.camFront=np.array([1.,0.,0.])
        self.camUp=np.array([0.,1.,0.])
        self.IsOrtho=False
        self.view = [
            self.camPos,
            self.camPos+self.camFront,
            self.camUp
        ]
        self.cursorShouldHide=False
        self.mouseX=constants.SCREEN_WIDTH/2.
        self.mouseY=constants.SCREEN_HEIGHT/2.

controller=Controller()

#Funcion para manejar el movimiento del mouse
def cursor_pos_callback(window,x,y):
    global controller
    #offsetX y offsetY muestran que tanto se ha movido el mouse desde el ultimo swap de buffers
    offsetX=controller.mouseX - x
    offsetY=y - controller.mouseY
    #x e y son las nuevas coordenadas actuales del mouse
    controller.mouseX=x
    controller.mouseY=y
    #Los offset se multiplican para tener un movimiento que no sea extremedamente brusco
    sensitivity=0.4
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

    if action != glfw.PRESS:
        return

    global controller
    
    if key==glfw.KEY_SPACE and action==glfw.PRESS:
        controller.IsOrtho=not controller.IsOrtho

    if not controller.IsOrtho:
        if key==glfw.KEY_LEFT_SHIFT and (action==glfw.PRESS or action==glfw.REPEAT):
            controller.camSpeed*=1.5
        if key==glfw.KEY_W and (action==glfw.PRESS or action==glfw.REPEAT):
            controller.camPos+=controller.camFront*controller.camSpeed
        if key==glfw.KEY_S and (action==glfw.PRESS or action==glfw.REPEAT):
            controller.camPos-=controller.camFront*controller.camSpeed
        if key==glfw.KEY_A and (action==glfw.PRESS or action==glfw.REPEAT):
            sidewayVector=np.cross(controller.camFront,controller.camUp)
            sidewayVector/=np.linalg.norm(sidewayVector)
            controller.camPos-=(sidewayVector*controller.camSpeed)
        if key==glfw.KEY_D and (action==glfw.PRESS or action==glfw.REPEAT):
            sidewayVector=np.cross(controller.camFront,controller.camUp)
            sidewayVector/=np.linalg.norm(sidewayVector)
            controller.camPos+=(sidewayVector*controller.camSpeed)


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

    #Color del fondo
    glClearColor(0.85, 0.85, 0.85, 1.0)

    #Testeo de profundidad para mostrar correctamente objetos 3D
    glEnable(GL_DEPTH_TEST)

    #Para que el mouse se quede dentro de la ventana y se pueda mover la camara libremente
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    #Para que la ventana registre los clicks del mouse
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    glfw.set_cursor_enter_callback(window, cursor_enter_callback)