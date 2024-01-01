from flask import Flask, render_template, Response
import cv2
import numpy as np
import threading
from time import sleep

app = Flask(__name__)
contAzul = 0
contAmarillo = 0

blueDark = np.array([100, 100, 20], np.uint8)
blueLight = np.array([125, 255, 255], np.uint8)
yellowDark = np.array([15, 100, 20], np.uint8)
yelloLight = np.array([45, 255, 255], np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX

azulLock = threading.Lock()
amarilloLock = threading.Lock()

enMovimiento = threading.Lock()


def azulDetectado():
    with azulLock:
        global contAzul
        print("Azul Detectado")
        sleep(2)
        contAzul = 0
        print("Funcion terminada")


def amarilloDetectado():
    with amarilloLock:
        global contAmarillo
        print("Amarillo Detectado")
        sleep(2)
        contAmarillo = 0
        print("Funcion terminada")


def draw(mask, color, name, frame):
    contour, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contour:
        area = cv2.contourArea(c)
        if area > 3000:
            M = cv2.moments(c)
            if M["m00"] == 0:
                M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M['m01'] / M['m00'])
            newContour = cv2.convexHull(c)
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
            cv2.putText(frame, name, (x + 10, y), font,
                        0.75, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.drawContours(frame, [newContour], 0, color, 3)

            global contAzul
            global contAmarillo
            if (name == "Azul"):
                contAzul = contAzul + 1
                contAmarillo = 0
                if (contAzul >= 50):
                    contAzul = 0
                    threading.Thread(target=azulDetectado).start()
            if (name == "Amarillo"):
                contAmarillo = contAmarillo + 1
                contAzul = 0
                if (contAmarillo >= 50):
                    contAmarillo = 0
                    threading.Thread(target=amarilloDetectado).start()


@app.route('/')
def index():
    return render_template('index.html')


def generate_frames():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        if ret:
            frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            maskAzul = cv2.inRange(frameHSV, blueDark, blueLight)
            maskAmarillo = cv2.inRange(frameHSV, yellowDark, yelloLight)

            draw(maskAzul, (255, 0, 0), "Azul", frame)
            draw(maskAmarillo, (0, 255, 255), "Amarillo", frame)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
