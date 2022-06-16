import constants
import numpy as np

#Clase para manejar la camara y movimiento
class Controller:
    def __init__(self):
        self.cameraPhiAngle = 0
        self.cameraThetaAngle = 0
        self.camBaseSpeed=0.5
        self.camSpeed= 0.7
        self.camPos=np.array([4,0.2,0.0])
        self.camFront=np.array([1.,0.,0.])
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