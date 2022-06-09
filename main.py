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
        self.strafeSpeed = 200./1280.
        self.forwardSpeed = 200./1280.
        self.currentStrafeSpeed = 0
        self.currentForwardSpeed = 0
        self.camPos=[0.,0.,0.]
        self.camFront=[1.,0.,0.]
        self.camUp=[0.,0.,1.]
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

    movementSpeed=np.array([0.,0.,0.])
    forwardSpeed=np.array([0.,0.,0.])
    strafeSpeed=np.array([0.,0.,0.])
    if key==glfw.KEY_LEFT_SHIFT and action==glfw.PRESS:
        controller.currentForwardSpeed*=2
        controller.currentStrafeSpeed*=2
    if key==glfw.KEY_W and action==glfw.PRESS:
        forwardSpeed=np.array(controller.camFront)/np.linalg.norm(np.array(controller.camFront))
        forwardSpeed*=controller.currentForwardSpeed
    if key==glfw.KEY_S and action==glfw.PRESS:
        forwardSpeed=np.array(controller.camFront)/np.linalg.norm(np.array(controller.camFront))
        forwardSpeed*=-controller.currentForwardSpeed
    if key==glfw.KEY_A and action==glfw.PRESS:
        strafeSpeed=np.array(controller.camFront)/np.linalg.norm(np.array(controller.camFront))
        strafeSpeed*=controller.currentStrafeSpeed
        rotacionIzquierda=tr.rotationZ(-np.pi/2)
        strafeSpeed=tr.matmul(rotacionIzquierda,strafeSpeed)
    if key==glfw.KEY_D and action==glfw.PRESS:
        strafeSpeed=np.array(controller.camFront)/np.linalg.norm(np.array(controller.camFront))
        strafeSpeed*=controller.currentStrafeSpeed
        rotacionIzquierda=tr.rotationZ(np.pi/2)
        strafeSpeed=tr.matmul(rotacionIzquierda,strafeSpeed)
    movementSpeed=forwardSpeed+strafeSpeed
    if not np.all(movementSpeed==0):
        movementSpeed/=np.linalg.norm(movementSpeed)
        movementSpeed=movementSpeed.tolist()
        controller.camPos+=movementSpeed


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

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)