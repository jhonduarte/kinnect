class BlobAnalysis:
      def__init__(self, BW): #Constructor. BW es una imagen binaria en forma de una matriz numpy
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
                try:
                    m10 = int(cv.GetSpatialMoment(m,1,0))
                    m00 = int(cv.GetSpatialMoment(m,0,0))
                    m01 = int(cv.GetSpatialMoment(m,0,1))
                    centroid.append(cv.Convexhull2(cs,cv.CreateMemStorage(),return_points=True) #Busca el convezo de cd en CvSeq
                    convexHull = cv.ConvexHull2(cs,cv.CreateMemStorage(),return_points=True) #Agrega el formulario de lista ConvexHull a la lista cHull
                    cHullArea.append(cv.ContourArea(convexHull)) #Agrega el formulario de lista de la envolvente convexa a la lista cHull
                    cHull.append(list(convexHull)) #Agrega el formulario de lista del contorno a la lista de contornos
                    contours.append(list(cs)) 
                    counter += 1 #Añade al counter para ver cuantos pixeles están allí
                except:
                    pass
            cs = cs.h_next()              
