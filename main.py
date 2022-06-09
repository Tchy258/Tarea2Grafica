import glfw
from OpenGL.GL import *
from basic_shapes import createSphere,createPrism
from gpu_shape import GPUShape
from easy_shaders import SimpleModelViewProjectionShaderProgram
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

    movementSpeed=[0.,0.,0.]

    if key==glfw.KEY_W and action==glfw.PRESS:
        forwardSpeed=np.array(controller.camFront)/np.linalg(np.array(controller.camFront))
        forwardSpeed*=controller.forwardSpeed
    if key==glfw.KEY_S and action==glfw.PRESS:
        forwardSpeed=np.array(controller.camFront)/np.linalg(np.array(controller.camFront))
        forwardSpeed*=-controller.forwardSpeed
        