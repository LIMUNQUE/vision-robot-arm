# Llamamos a las librerias
import RPi.GPIO as GPIO
from flask import Flask, render_template, Response
import cv2
import numpy as np
import threading
from time import sleep
import firebase_admin
from firebase_admin import db, credentials
import os


def test():
    os.system('ngrok http --domain=optionally-national-osprey.ngrok-free.app 5000')


servo1 = 18  # GPIO Pin where sero is connected
servo2 = 12
servo3 = 15
servo4 = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1, GPIO.OUT)
GPIO.setup(servo2, GPIO.OUT)
GPIO.setup(servo3, GPIO.OUT)
GPIO.setup(servo4, GPIO.OUT)


p1 = GPIO.PWM(servo1, 50)  # PWM channel at 50 Hz frequency
p2 = GPIO.PWM(servo2, 50)
p3 = GPIO.PWM(servo3, 50)
p4 = GPIO.PWM(servo4, 50)
GPIO.setwarnings(False)
p1.start(0)  # Zero duty cycle initially
p2.start(0)
p3.start(0)
p4.start(0)

# Autenticate to firebase
cred = credentials.Certificate('/home/pi/Desktop/pyProject/credentials.json')

firebase_admin.initialize_app(
    cred, {"databaseURL": "https://cursoesp32-523d8-default-rtdb.firebaseio.com/"})

# Variables de entorno
app = Flask(_name_)
contAzul = 0
contAmarillo = 0
manual_control_active = False
# cap = cv2.VideoCapture(0)
# Mapas de colores
blueDark = np.array([100, 100, 20], np.uint8)
blueLight = np.array([125, 255, 255], np.uint8)
yellowDark = np.array([15, 100, 20], np.uint8)
yelloLight = np.array([45, 255, 255], np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
# Bloqueo de hilos
enMovimiento = threading.Lock()


def azulDetectado():  # Funcion al detectar un color
    # Se bloquea el hilo para que no se ejecute mas de una vez
    with enMovimiento:
        global contAzul
        print("Azul Detectado")
        # Empieza a moverse
        # Empieza a moverse
        p1.ChangeDutyCycle(4)  # 1 to 12.5
        sleep(0.5)
        p1.ChangeDutyCycle(0)
        sleep(0.1)
        p2.ChangeDutyCycle(9)
        sleep(0.5)
        p2.ChangeDutyCycle(0)
        sleep(0.1)
        p4.ChangeDutyCycle(6)
        sleep(2)
        p4.ChangeDutyCycle(0)
        sleep(0.1)

        # Agarra
        p4.ChangeDutyCycle(2)
        sleep(0.5)
        p4.ChangeDutyCycle(0)
        sleep(0.1)
        p1.ChangeDutyCycle(10)
        sleep(0.5)
        p1.ChangeDutyCycle(0)
        sleep(0.1)
        p2.ChangeDutyCycle(5)
        sleep(0.5)
        p2.ChangeDutyCycle(0)
        sleep(0.1)
        p4.ChangeDutyCycle(5)
        sleep(0.5)
        p4.ChangeDutyCycle(0)
        sleep(0.1)
        p2.ChangeDutyCycle(9)
        sleep(0.5)
        p2.ChangeDutyCycle(0)
        sleep(0.1)
        p1.ChangeDutyCycle(4)
        sleep(0.5)
        p1.ChangeDutyCycle(0)
        sleep(0.1)
        contAzul = 0
        print("Funcion terminada")


def amarilloDetectado():  # Se termina el bloqueo
    with enMovimiento:
        global contAmarillo
        print("Amarillo Detectado")

        # Empieza a moverse
        p1.ChangeDutyCycle(4)  # 1 to 12.5
        sleep(0.5)
        p1.ChangeDutyCycle(0)
        sleep(0.1)
        p2.ChangeDutyCycle(9)
        sleep(0.5)
        p2.ChangeDutyCycle(0)
        sleep(0.1)
        p4.ChangeDutyCycle(6)
        sleep(2)
        p4.ChangeDutyCycle(0)
        sleep(0.1)

        # Agarra
        p4.ChangeDutyCycle(2)
        sleep(0.5)
        p4.ChangeDutyCycle(0)
        sleep(0.1)
        p1.ChangeDutyCycle(10)
        sleep(0.5)
        p1.ChangeDutyCycle(0)
        sleep(0.1)
        p4.ChangeDutyCycle(5)
        sleep(0.5)
        p4.ChangeDutyCycle(0)
        sleep(0.1)
        p1.ChangeDutyCycle(4)
        sleep(0.5)
        p1.ChangeDutyCycle(0)
        sleep(0.1)

        # Funcion terminada
        contAmarillo = 0
        print("Funcion terminada")


def draw(mask, color, name, frame):  # Funcion de clasificaciï¿½n de colores
    contour, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    global contAzul
    global contAmarillo
    for c in contour:
        area = cv2.contourArea(c)
        if (area > 3000):
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
            # Contador de frames para llamar a la funcion de deteccion

            if (name == "Azul"):
                contAzul = contAzul + 1
                contAmarillo = 0
                if (contAzul >= 20):
                    contAzul = 0
                    threading.Thread(target=azulDetectado).start()
            if (name == "Amarillo"):
                contAmarillo = contAmarillo + 1
                contAzul = 0
                if (contAmarillo >= 20):
                    contAmarillo = 0
                    threading.Thread(target=amarilloDetectado).start()


@app.route('/')
def index():
    return render_template('index.html')


def generate_frames():  # Funcion de captura de video
    cap = cv2.VideoCapture(0)
    while True:
        if db.reference("/Valor").get() == "1":
            threading.Thread(target=manualControl).start()
        ret, frame = cap.read()
        if ret:
            if db.reference("/Valor").get() == "2":
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


def manualControl():
    global manual_control_active
    # Se obtienen los valores del database
    motor1 = db.reference("/Motor1").get()
    motor2 = db.reference("/Motor2").get()
    motor3 = db.reference("/Motor3").get()
    motor4 = db.reference("/Motor4").get()
    if (manual_control_active == False):
        while db.reference("/Valor").get() == "1":
            manual_control_active = True
            # Detect changes in database
            if motor1 != db.reference("/Motor1").get():
                motor1 = db.reference("/Motor1").get()
                print("Motor1: ", int(motor1))
                p1.ChangeDutyCycle(int(motor1))  # 1 to 12.5
                sleep(0.5)
                p1.ChangeDutyCycle(0)
            if motor2 != db.reference("/Motor2").get():
                motor2 = db.reference("/Motor2").get()
                print("Motor2: ", int(motor2))
                p2.ChangeDutyCycle(int(motor2))
                sleep(0.5)
                p2.ChangeDutyCycle(0)
            if motor3 != db.reference("/Motor3").get():
                motor3 = db.reference("/Motor3").get()
                print("Motor3: ", int(motor3))
                p3.ChangeDutyCycle(int(motor3))
                sleep(0.5)
                p3.ChangeDutyCycle(0)
            if motor4 != db.reference("/Motor4").get():
                motor4 = db.reference("/Motor4").get()
                print("Motor4: ", int(motor4))
                p4.ChangeDutyCycle(int(motor4))
                sleep(0.5)
                p4.ChangeDutyCycle(0)
        manual_control_active = False


if _name_ == '_main_':
    # threading.Thread(target=test).start()
    manualControl()
    app.run(debug=True)
