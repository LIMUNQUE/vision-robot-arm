import cv2
import numpy as np
import imutils
print("Librerias leídas")

cap = cv2.VideoCapture(0)
cap.set(4, 480)

# Obtener las dimensiones del video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

center_x = width // 2
center_y = height // 2

box_x1 = center_x - width // 4
box_y1 = center_y - height // 4
box_x2 = center_x + width // 4
box_y2 = center_y + height // 4

color = (0, 0, 0) # Color Border
thickness = 3 # 3 píxeles

def draw_frame(nombre,color, cnts):
    for c in cnts:
        area = cv2.contourArea(c)
        if area>5000:
            M = cv2.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])
             # Comprobar si el centro del objeto está dentro del rectángulo
            if box_x1 < cx < box_x2 and box_y1 < cy < box_y2:
                cv2.drawContours(frame, [c], -1, color, 3)
                cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
                cv2.putText(frame, nombre, (cx - 20, cy - 20), cv2.FONT_ITALIC, 2, (255, 255, 255), 2)

while True:

    ret, frame = cap.read()

    # Comprobar si se ha leído correctamente el fotograma
    if ret:
        # Dibujar el cuadro en el fotograma
        cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), color, thickness)


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #AMARILLO
    amarillo_osc = np.array([25, 70, 120])
    amarillo_cla = np.array([35, 255, 255])

    #ROJO
    rojo_osc = np.array([0, 50, 120])
    rojo_cla = np.array([10, 255, 255])

    #VERDE
    verde_osc = np.array([40, 70, 80])
    verde_cla = np.array([70, 255, 255])

    #AZUL
    azul_osc = np.array([90, 60, 0])
    azul_cla = np.array([121, 255, 255])

    cara1 = cv2.inRange(hsv, amarillo_osc, amarillo_cla)
    cara2 = cv2.inRange(hsv, rojo_osc, rojo_cla)
    cara3 = cv2.inRange(hsv, verde_osc, verde_cla)
    cara4 = cv2.inRange(hsv, azul_osc, azul_cla)

    cnts1 = cv2.findContours(cara1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts1 = imutils.grab_contours(cnts1)

    cnts2 = cv2.findContours(cara2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = imutils.grab_contours(cnts2)

    cnts3 = cv2.findContours(cara3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts3 = imutils.grab_contours(cnts3)

    cnts4 = cv2.findContours(cara4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    cnts4 = imutils.grab_contours(cnts4)

    draw_frame("Amarillo", (30, 255, 255), cnts1)
    draw_frame("Rojo", (0, 0, 255), cnts2)
    draw_frame("Verde", (0, 255, 0), cnts3)
    draw_frame("Azul", (255, 0, 0), cnts4)
    

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()