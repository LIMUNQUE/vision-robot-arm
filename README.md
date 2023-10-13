# vision-robot-arm

The purpose of this project is to create a robot arm with an esp32-cam, using artificial vision from opencv.
It will be able to classify objects by color and other characteristics in order to pick and drop them in the correct place.

In a close future we'll add micro-ros for improve communication between server and the microcontroller.

<picture> <img src="https://i.ibb.co/Zf3y1xT/structure.png" width = 500px></picture>

## Microcontroller Code

Install the esp32 cam library on the arduino IDE and the "esp32cam-main" libraly locale on src/libreria_arduino.
Select the AI thinker esp cam
You can change the name and password network or create another with the same characteristics.

<picture> <img src="https://i.ibb.co/5Y5FcD1/WM-Screenshots-20231013165800.png" width = 300px></picture>


Upload the code on the board when it is finished you'll have to enter as a url the ip address the monitor showed, next select the format you want to show on screen.

<picture> <img src="https://i.ibb.co/G7h6Tkf/face.png" width = 500px></picture>

## Installation procedure

For the strucutre of the python part of the proyect we are using the python manager rye.

##### 1. Download the project

You can download the project as a zip file using the download button at the beginning. Additionally, you can clone the project with git using the project's url.

##### 2. Download rye

Follow the steps of the [guide](https://rye-up.com/guide/installation/)
remember to add it to the path

##### 3. Install the dependencies

Using the cmd locate the folder where the project is and type the next command:

```
rye sync
```

it will start to install all the dependencies in the .toml file.

Finally you can start the project typing:

```
rye run dev
```
