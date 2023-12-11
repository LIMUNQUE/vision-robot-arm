import cv2
import numpy as np
import time
import serial

esp = serial.Serial("COM9", 115200)


def draw(mask, color, name):
    contour, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                  cv2.CHAIN_APPROX_SIMPLE)
    for c in contour:
        area = cv2.contourArea(c)
        if area > 3000:
            M = cv2.moments(c)
            if (M["m00"] == 0):
                M["m00"] = 1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            newContour = cv2.convexHull(c)
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
            cv2.putText(frame, name, (x+10, y),
                        font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.drawContours(frame, [newContour], 0, color, 3)
            # run a function depending on the color
            # Use esp.write and send the name value to the arduino
            esp.write(name.encode())
            time.sleep(0.2)
            esp.close()


# cap = cv2.VideoCapture(0)
url = 'http://192.168.100.91/cam.mjpeg'
cap = cv2.VideoCapture(url)  # Crear objeto VideoCapture


blueDark = np.array([100, 100, 20], np.uint8)
blueLight = np.array([125, 255, 255], np.uint8)
yellowDark = np.array([15, 100, 20], np.uint8)
yelloLight = np.array([45, 255, 255], np.uint8)
redDark1 = np.array([0, 100, 20], np.uint8)
redLight1 = np.array([5, 255, 255], np.uint8)
redDark2 = np.array([175, 100, 20], np.uint8)
redLight2 = np.array([179, 255, 255], np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, frame = cap.read()
    if ret == True:
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        maskAzul = cv2.inRange(frameHSV, blueDark, blueLight)
        maskAmarillo = cv2.inRange(frameHSV, yellowDark, yelloLight)
        maskRed1 = cv2.inRange(frameHSV, redDark1, redLight1)
        maskRed2 = cv2.inRange(frameHSV, redDark2, redLight2)
        maskRed = cv2.add(maskRed1, maskRed2)
        draw(maskAzul, (255, 0, 0), 1)  # Azul
        draw(maskAmarillo, (0, 255, 255), 2)  # Amarillo
        draw(maskRed, (0, 0, 255), 3)  # Rojo
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
cap.release()
cv2.destroyAllWindows()
