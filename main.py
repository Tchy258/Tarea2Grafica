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
        self.cameraPhiAngle = -np.pi/2
        self.cameraThetaAngle = 0
        self.camSpeed= 0.5
        self.camPos=[0.,0.,0.]
        self.camFront=[1.,0.,0.]
        self.camUp=[0.,0.,1.]
        self.IsOrtho=False
        self.view = [
            self.camPos,
            self.camPos+self.camFront,
            self.camUp
        ]

controller=Controller()

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
            sidewayVector=np.cross(np.array(controller.camFront),np.array(controller.camUp))
            sidewayVector/=np.linalg.norm(sidewayVector)
            controller.camPos-=(sidewayVector*controller.camSpeed).tolist() 
        if key==glfw.KEY_D and (action==glfw.PRESS or action==glfw.REPEAT):
            sidewayVector=np.cross(np.array(controller.camFront),np.array(controller.camUp))
            sidewayVector/=np.linalg.norm(sidewayVector)
            controller.camPos+=(sidewayVector*controller.camSpeed).tolist()


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