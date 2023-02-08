import cv2
import os
import numpy as np
from pathlib import Path
import pyttsx3

#por que no hay sonido?, segui el tutorial al pie de la letra

aqui=Path(__file__).resolve().parent

ruta= f"{aqui}\\billetes\\"

def mascara(imagen):
    hsv=cv2.cvtColor(imagen,cv2.COLOR_BGR2HSV)
    engine=pyttsx3.init()
    voz="spanish-latin-am"
    engine.setProperty("voice",voz)
    rate=engine.getProperty("rate")
    engine.setProperty("rate",rate+10)
    filas,columnas,_=imagen.shape

    pixeles=filas*columnas

    #para 10 soles
    verdeMinimo=np.array([40,50,50])
    verdeMaximo=np.array([80,255,255])
    mascaraVerde=cv2.inRange(hsv,verdeMinimo,verdeMaximo)

    #para 20 soles
    marronMinimo=np.array([10,50,50])
    marronMaximo=np.array([20,255,255])
    mascaraMarron=cv2.inRange(hsv,marronMinimo,marronMaximo)

    #para 50 soles
    rosaMinimo=np.array([150,50,50])
    rosaMaximo=np.array([180,255,255])
    mascaraRosa=cv2.inRange(hsv,rosaMinimo,rosaMaximo)

    #para 100 soles
    azulMinimo=np.array([100,50,50])
    azulMaximo=np.array([140,255,255])
    mascaraAzul=cv2.inRange(hsv,azulMinimo,azulMaximo)    

    if np.count_nonzero(mascaraVerde)>0.1*pixeles:
        mensaje="El billete es de 10 soles"
        mascaraFinal=mascaraVerde

    if np.count_nonzero(mascaraMarron)>0.05*pixeles:
        mensaje="El billete es de 20 soles"
        mascaraFinal=mascaraMarron

    if np.count_nonzero(mascaraRosa)>0.05*pixeles:
        mensaje="El billete es de 50 soles"
        mascaraFinal=mascaraRosa
    
    if np.count_nonzero(mascaraAzul)>0.05*pixeles:
        mensaje="El billete es de 100 soles"
        mascaraFinal=mascaraAzul
    
    resultado= cv2.bitwise_and(imagen,imagen,mask=mascaraFinal)


    cv2.imshow("Imagen Original",imagen)
    #cv2.imshow("Resultado",resultado)
    
    #print(mensaje)
    engine.say(mensaje)
    engine.runAndWait()
    cv2.waitKey(0)

for nombre in os.listdir(ruta):
    if nombre.endswith('.jpg'):
        rutaImagen=os.path.join(ruta,nombre)
        imagen=cv2.imread(rutaImagen)
        mascara(imagen)

cv2.destroyAllWindows()