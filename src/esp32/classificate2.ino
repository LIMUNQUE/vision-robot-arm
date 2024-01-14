/**
 * 
 * The PSRAM version can be found in my
 * "ESP32S3 Camera Mastery" course
 * at https://dub.sh/ufsDj93
 *
 */
#include <ESP32-CAM_inferencing.h>
#include <eloquent_esp32cam.h>
#include <eloquent_esp32cam/edgeimpulse/fomo.h>
#include <WiFi.h>
#include <ESP32Firebase.h>
#include <ESP32Servo.h>

int contBlue=0;
int contBrown=0;

using eloq::camera;
using eloq::ei::fomo;

#define _SSID "NETLIFE-JSanchez1"
#define _PASSWORD "1203428972"
#define REFERENCE_URL "sistemas-embebidos-posiciones-default-rtdb.firebaseio.com/" // Firebase project url

Servo myservo;
Servo myservo2;
Servo myservo3;
Servo myservo4;
Firebase firebase(REFERENCE_URL);

void setup() {
  delay(3000);
  Serial.begin(115200);
  Serial.println("__EDGE IMPULSE FOMO (NO-PSRAM)__");
  Serial.setDebugOutput(true);

    // camera settings
    // replace with your own model!
  camera.pinout.aithinker();
  camera.brownout.disable();
    // NON-PSRAM FOMO only works on 96x96 (yolo) RGB565 images
  camera.resolution.yolo();
  camera.pixformat.rgb565();

    // init camera
  while (!camera.begin().isOk())
      Serial.println(camera.exception.toString());

  Serial.println("Camera OK");
  Serial.println("Put object in front of camera");

  // Seteo de periodo
  myservo.setPeriodHertz(50);
  myservo2.setPeriodHertz(50);
  myservo3.setPeriodHertz(50);
  myservo4.setPeriodHertz(50);

  // Asignación de pines
  myservo.attach(12, 1000, 2000);  // Hombro
  myservo2.attach(13, 1000, 2000); // Codo
  myservo3.attach(14, 1000, 2000); // Muñeca
  myservo4.attach(27, 1000, 2000); // Pinza

  WiFi.begin(_SSID, _PASSWORD);
  WiFi.setSleep(false);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
}


void loop() {

  // capture picture
    if (!camera.capture().isOk()) {
      Serial.println(camera.exception.toString());
      return;
    }

    // run FOMO
    if (!fomo.run().isOk()) {
      Serial.println(fomo.exception.toString());
      return;
    }

    // if no object is detected, return
    if (!fomo.foundAnyObject())
      return;

    // if you expect to find a single object, use fomo.first
    Serial.printf(
      "Found %s. "
      "Proba is %.2f\n",
      fomo.first.label,
      fomo.first.proba
    );


    //Detectar clasificación de colores para mover motores
    if(fomo.first.label=="Blue"){
      contBlue+=1;
      contBrown=0;
      if(contBlue>=5){
        moverAzul();
      }
    }

    if(fomo.first.label=="Cafe"){
      contBlue=0;
      contBrown+=1;
      if(contBrown>=5){
        moverCafe();
      }
    }
}

void moverAzul(){
  Serial.println("Azul detectado");
  enEspera();
  myservo3.write(180);
  delay(10);
  myservo.write(180);
  delay(10);
  enEspera();
}
void moverCafe(){
  Serial.println("Cafe detectado");
  enEspera();
  myservo3.write(180);
  delay(10);
  myservo.write(100);
  delay(10);
  enEspera();
}

void enEspera(){
  myservo.write(0);
  delay(10);
  //myservo.write2(0);
  myservo3.write(0);
  myservo4.write(0);
}