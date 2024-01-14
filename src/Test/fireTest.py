import firebase_admin
from firebase_admin import db, credentials

# Autenticate to firebase
cred = credentials.Certificate(
    './credentials.json')

firebase_admin.initialize_app(
    cred, {"databaseURL": "https://cursoesp32-523d8-default-rtdb.firebaseio.com/"})


# db.reference("/Motor1").set(45)  # Value changed

# At the beginning, get all values from database
motor1 = db.reference("/Motor1").get()
motor2 = db.reference("/Motor2").get()
motor3 = db.reference("/Motor3").get()
motor4 = db.reference("/Motor4").get()


while db.reference("/Valor").get() == "1":
    # Detect changes in database
    if motor1 != db.reference("/Motor1").get():
        motor1 = db.reference("/Motor1").get()
        print("Motor1: ", int(motor1))
    if motor2 != db.reference("/Motor2").get():
        motor2 = db.reference("/Motor2").get()
        print("Motor2: ", int(motor2))
    if motor3 != db.reference("/Motor3").get():
        motor3 = db.reference("/Motor3").get()
        print("Motor3: ", int(motor3))
    if motor4 != db.reference("/Motor4").get():
        motor4 = db.reference("/Motor4").get()
        print("Motor4: ", int(motor4))
