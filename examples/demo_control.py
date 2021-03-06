from freenect import sync_get_depth as get_depth
import numpy as np
import pygame
from Xlib import X, display
import Xlib.XK
import Xlib.error
import Xlib.ext.xtest

class BlobAnalysis:
      def __init__(self, BW):#Constructor. BW es una imagen binaria en forma de una matriz numpy
            self.BW=BW
            cs = cv.FindContours(cv.fromarray(self.BW.astype(np.uint8)),cv.CreateMemStorage(),mode = cv.CV_RETR_EXTERNAL) #Encuentra los contornos
            counter = 0
            centroid = list()
            cHull = list()
            contours = list()
            ChullArea = list()
            contourArea = list()
            
            while cs:
                  if asb(cv.ContourArea(cs)) > 2000 #Filtra contornos pequeños de mas de 2000 pixeles en el área
                        ContourArea.append(cv.ContourArea(cs)) #Añade ContourArea con el nuevo contorno
                        m = cv.Moments(cs)
                        try:
                              m10 = int(cv.GetSpatialMoment(m,1,0))
                              m00 = int(cv.GetSpatialMoment(m,0,0))
                              m01 = int(cv.GetSpatialMoment(m,0,1))
                              centroid.append(cv.Convexhull2(cs,cv.CreateMemStorage(),return_points=True) #Busca el convezo de cd en CvSeq                    convexHull = cv.ConvexHull2(cs,cv.CreateMemStorage(),return_points=True) #Agrega el formulario de lista ConvexHull a la lista cHull             cHullArea.append(cv.ContourArea(convexHull)) #Agrega el formulario de lista de la envolvente convexa a la lista cHull
                              cHull.append(list(convexHull)) #Agrega el formulario de lista del contorno a la lista de contornos
                              contours.append(list(cs)) 
                              counter += 1 #Añade al counter para ver cuantos pixeles están all
                        except:
                              pass
                  cs = cs.h_next()                      
        self.centroid = centroid
        self.counter = counter
        self.cHull = cHull
        self.contours = contours
        self.cHullArea = cHullArea
        self.contourArea = contourArea

d = display.Display() #Pantalla de referencia para la manipulación Xlib
def move_mouse(x,y):#Mueve el ratón en (x,y). "x" y "y" son enteros
    s = d.screen()
    root = s.root
    root.warp_pointer(x,y)
    d.sync()
                                        
def click_down(button):#Simula un clic abajo. Button es un entero
    Xlib.ext.xtest.fake_input(d,X.ButtonPress, button)
    d.sync()
    
def click_up(button): #Simula un clic arriba. Button es un entero
    Xlib.ext.xtest.fake_input(d,X.ButtonRelease, button)
    d.sync()

def cacheAppendMean(cache, val):
    cache.append(val)
    del cache[0]
    return np.mean(cache) 
                                    
def hand_tracker():
    (depth,_) = get_depth()
    cHullAreaCache = constList(5,12000)
    areaRatioCache = constList(5,1)
    centroidList = list() #Iniciar centroid list
    #Colores basicos RGB
    BLACK = (0,0,0)
    RED = (255,0,0)
    GREEN = (0,255,0)
    PURPLE = (255,0,255)
    BLUE = (0,0,255)
    WHITE = (255,255,255)
    YELLOW = (255,255,0)
    pygame.init() #Inicializar pygame
    xSize,ySize = 640,480 #Ajusta resolución de la pantalla
    screen = pygame.display.set_mode((xSize,ySize),pygame.RESIZABLE) #Crea la interfaz principal
    screenFlipped = pygame.display.set_mode((xSize,ySize),pygame.RESIZABLE) 
    screen.fill(BLACK) #Hacer fondo negro
    done = False #Repetir boolean --> Le dice al programa cuando finalizar
    dummy = False
    while not done:
        screen.fill(BLACK)
        (depth,_) = get_depth() #Obtener la profundidad del Kinect 
        depth = depth.astype(np.float32) #Convertir la profunidad del objeto a 32 bits
        _,depthThresh = cv2.threshold(depth, 600, 255, cv2.THRESH_BINARY_INV)
        _,back = cv2.threshold(depth, 900, 255, cv2.THRESH_BINARY_INV)
        blobData = BlobAnalysis(depthThresh) #Crear blobData object usando BlobAnalysis class
        blobDataBack = BlobAnalysis(back)
        
        for cont in blobDataBack.contours: #Repite los contornos en el fondo
            pygame.draw.lines(screen,YELLOW,True,cont,3)
        for i in range(blobData.counter): #Repite 
            pygame.draw.circle(screen,BLUE,blobData.centroid[i],10)
            centroidList.append(blobData.centroid[i])
            pygame.draw.lines(screen,RED,True,blobData.cHull[i],3)
            pygame.draw.lines(screen,GREEN,True,blobData.contours[i],3)
            for tips in blobData.cHull[i]:
                pygame.draw.circle(screen,PURPLE,tips,5)
                                    
 pygame.display.set_caption('Kinect Tracking') 
        del depth
        screenFlipped = pygame.transform.flip(screen,1,0)
        screen.blit(screenFlipped,(0,0)) 
        pygame.display.flip() 
                                    
        try:
            centroidX = blobData.centroid[0][0]
            centroidY = blobData.centroid[0][1]
            if dummy:
                mousePtr = display.Display().screen().root.query_pointer()._data #Gets current mouse attributes
                dX = centroidX - strX 
                dY = strY - centroidY 
                if abs(dX) > 1: 
                    mouseX = mousePtr["root_x"] - 2*dX 
                if abs(dY) > 1:
                    mouseY = mousePtr["root_y"] - 2*dY 
                move_mouse(mouseX,mouseY)
                strX = centroidX 
                strY = centroidY 
                cArea = cacheAppendMean(cHullAreaCache,blobData.cHullArea[0]) 
                areaRatio = cacheAppendMean(areaRatioCache, blobData.contourArea[0]/cArea)
                if cArea < 10000 and areaRatio > 0.82:
                    click_down(1)
                else:
                    click_up(1)
            else:
                strX = centroidX 
                strY = centroidY 
                dummy = True 
        except:
            dummy = False
            
        for e in pygame.event.get():
            if e.type is pygame.QUIT:
                done = True

try: 
    hand_tracker()
except: 
    pass
