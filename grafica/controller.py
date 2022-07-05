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

#Todas las funciones para curvas se extrajeron del archivo auxiliarT5.py de u-cursos

#Función para generar el vector cuyo producto con la matriz de bezier da la posición
def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T


#Función que genera una matriz para una curva de bezier según sus 4 puntos de control
def bezierMatrix(P0, P1, P2, P3):
    
    # Generate a matrix concatenating the columns
    G = np.concatenate((P0, P1, P2, P3), axis=1)

    # Bezier base matrix is a constant
    Mb = np.array([[1, -3, 3, -1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]])
    
    return np.matmul(G, Mb)

#Función para evaluar la curva, es decir, dado un t entre 0 y 1, retorna coordenadas
#correspondientes a una posición en la curva
def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)
    
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T
        
    return curve

#Función para generar la curva que va a recorrer el auto
def generateCurve(N):
    
    #La curva está dividida en 8 tramos
    #El primer tramo parte por abajo y va derecho
    R0 = np.array([[-1, 0.2, -1.8]]).T
    R1 = np.array([[-3, 0.2, -1.8]]).T
    R2 = np.array([[-5, 0.2, -1.8]]).T
    R3 = np.array([[-8, 0.2, -1.8]]).T
    
    M1 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve1 = evalCurve(M1, N)

    #Aquí el auto dobla en la esquina inferior derecha de la escena (vista desde arriba)
    R0 = np.array([[-8, 0.2, -1.8]]).T
    R1 = np.array([[-11, 0.2, -1.8]]).T
    R2 = np.array([[-12.1, 0.2, -1.1]]).T
    R3 = np.array([[-12.3, 0.2, 0.1]]).T
    
    M2 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve2 = evalCurve(M2, N)

    #Luego sigue recto hacia arriba
    R0 = np.array([[-12.3, 0.2, 0.1]]).T
    R1 = np.array([[-12.3, 0.2, 4]]).T
    R2 = np.array([[-12.3, 0.2, 12]]).T
    R3 = np.array([[-12.3, 0.2, 18]]).T
    
    M3 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve3 = evalCurve(M3, N)

    #Dobla hacia la izquierda en la esquina superior derecha
    R0 = np.array([[-12.3, 0.2, 18.]]).T
    R1 = np.array([[-12.3, 0.2, 20]]).T
    R2 = np.array([[-9.3, 0.2, 20]]).T
    R3 = np.array([[-7.3, 0.2, 20]]).T
    
    M4 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve4 = evalCurve(M4, N)

    #Sigue derecho por la parte superior
    R0 = np.array([[-7.3, 0.2, 20.]]).T
    R1 = np.array([[-6, 0.2, 20]]).T
    R2 = np.array([[-5.5, 0.2, 20]]).T
    R3 = np.array([[-4.8, 0.2, 20]]).T
    
    M5 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve5 = evalCurve(M5, N)

    #Dobla hacia la parte diagonal y la recorre
    R0 = np.array([[-4.8, 0.2, 20.]]).T
    R1 = np.array([[-1.5, 0.2, 20]]).T
    R2 = np.array([[0.5, 0.2, 18]]).T
    R3 = np.array([[1.8, 0.2, 14]]).T

    M6 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve6 = evalCurve(M6, N)

    #Avanza hacia abajo
    R0 = np.array([[1.8, 0.2, 14.]]).T
    R1 = np.array([[1.8, 0.2, 10]]).T
    R2 = np.array([[1.8, 0.2, 6]]).T
    R3 = np.array([[1.8, 0.2, 2]]).T

    M7 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve7 = evalCurve(M7, N)

    #Dobla y vuelve a la posición inicial
    R0 = np.array([[1.8, 0.2, 2]]).T
    R1 = np.array([[1.8, 0.2, -1.1]]).T
    R2 = np.array([[0, 0.2, -1.8]]).T
    R3 = np.array([[-1, 0.2, -1.8]]).T

    M8 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve8 = evalCurve(M8, N)

    # Se concatenan todos los tramos para hacer una curva que recorre la escena
    C = np.concatenate((bezierCurve1,bezierCurve2,bezierCurve3, bezierCurve4, \
        bezierCurve5,bezierCurve6,bezierCurve7,bezierCurve8), axis=0)

    return C