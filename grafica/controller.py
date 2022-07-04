import grafica.constants as constants
import numpy as np

#Clase para manejar la camara y movimiento
class Controller:
    def __init__(self):
        self.cameraPhiAngle = 0
        self.cameraThetaAngle = 0
        self.camBaseSpeed=0.5
        self.camSpeed= 0.7
        self.camPos=np.array([-0.7,0.2,14.7])
        self.camFront=np.array([0.,1.,0.])
        self.camUp=np.array([0.,1.,0.])
        self.IsOrtho=False
        self.view = [
            self.camPos,
            self.camPos+self.camFront,
            self.camUp
        ]
        self.cursorShouldHide=True
        self.mouseX=constants.SCREEN_WIDTH/2.
        self.mouseY=constants.SCREEN_HEIGHT/2.
        self.flashlightOn=False

#Clase para contener todos los atributos de las luces
class Spotlight:
    def __init__(self):
        self.ambient = np.array([0,0,0])
        self.diffuse = np.array([0,0,0])
        self.specular = np.array([0,0,0])
        self.constant = 0
        self.linear = 0
        self.quadratic = 0
        self.position = np.array([0,0,0])
        self.direction = np.array([0,0,0])
        self.cutOff = 0
        self.outerCutOff = 0

class Car:
    def __init__(self):
        self.Pos=np.array([-4.71922016 , 0.2, -1.44114551])
        self.lights=False
        self.speed=2