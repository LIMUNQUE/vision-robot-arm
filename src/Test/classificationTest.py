import cv2
import numpy as np
import imutils
import threading
import time

print("Librerias leídas")

url = 'http://192.168.100.88/480x320.jpg'
cap = cv2.VideoCapture(url)  # Crear objeto VideoCapture


# Variable que servirá para bloquear la función
lock = threading.Lock()

winName = 'IP_CAM'
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)


# Obtener las dimensiones del video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

center_x = width // 2
center_y = height // 2

box_x1 = center_x - width // 4
box_y1 = center_y - height // 4
box_x2 = center_x + width // 4
box_y2 = center_y + height // 4

color = (0, 0, 0)  # Color Border
thickness = 3  # 3 píxeles

# Cuando un color se halla detectado se llama a la función


def color_detected(nombre):
    global lock

    if lock.locked():  # Si la función está bloqueada
        return
    lock.acquire()

    def mover_motores():
        time.sleep(5)
        print("Función finalizada")
        print()
        lock.release()  # Liberar la función después de esperar
    # Iniciar función asíncrona
    thread = threading.Thread(target=mover_motores)
    thread.start()
    print("Color detectado:", nombre)
    print("Moviendo Motores...")
    print()


def draw_frame(nombre, color, cnts):  # Se dibujan los contornos cuando se detecten
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 5000:
            M = cv2.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])
            # Comprobar si el centro del objeto está dentro del rectángulo
            if box_x1 < cx < box_x2 and box_y1 < cy < box_y2:
                cv2.drawContours(frame, [c], -1, color, 3)
                cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
                cv2.putText(frame, nombre, (cx - 20, cy - 20),
                            cv2.FONT_ITALIC, 2, (255, 255, 255), 2)
                # Llamar a la función que bloqueará el hilo
                color_detected(nombre)


while (1):

    cap.open(url)

    ret, frame = cap.read()

    if ret:
        cv2.rectangle(frame, (box_x1, box_y1),
                      (box_x2, box_y2), color, thickness)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # AMARILLO
    amarillo_osc = np.array([25, 70, 120])
    amarillo_cla = np.array([30, 255, 255])

    # AZUL
    azul_osc = np.array([90, 60, 0])
    azul_cla = np.array([255, 255, 186])

    cara1 = cv2.inRange(hsv, amarillo_osc, amarillo_cla)
    cara4 = cv2.inRange(hsv, azul_osc, azul_cla)

    cnts1 = cv2.findContours(cara1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts1 = imutils.grab_contours(cnts1)

    cnts4 = cv2.findContours(cara4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts4 = imutils.grab_contours(cnts4)

    draw_frame(1, (30, 255, 255), cnts1)  # Amarrillo
    draw_frame(2, (255, 0, 0), cnts4)  # Azul

    cv2.imshow(winName, frame)
    tecla = cv2.waitKey(1) & 0xFF

    if tecla == 27:
        break

cv2.destroyAllWindows()
