import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import imutils


class ColorTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Tracking App")

        self.video_source = 0  # Puedes cambiar esto si tu cámara tiene otro índice
        self.cap = cv2.VideoCapture(self.video_source)

        self.blue_dark = np.array([100, 100, 20], np.uint8)
        self.blue_light = np.array([125, 255, 255], np.uint8)
        self.yellow_dark = np.array([15, 100, 20], np.uint8)
        self.yellow_light = np.array([45, 255, 255], np.uint8)
        self.red_dark1 = np.array([0, 100, 20], np.uint8)
        self.red_light1 = np.array([5, 255, 255], np.uint8)
        self.red_dark2 = np.array([175, 100, 20], np.uint8)
        self.red_light2 = np.array([179, 255, 255], np.uint8)

        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=640, height=700)
        self.canvas.pack()

        self.quit_button = ttk.Button(
            self.root, text="Salir", command=self.quit_app)
        self.quit_button.pack()

        self.update()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            # Ajustar tamaño de la imagen
            # frame = cv2.resize(frame, (1280, 700))
            frame = imutils.resize(frame, width=640)
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask_blue = cv2.inRange(frame_hsv, self.blue_dark, self.blue_light)
            mask_yellow = cv2.inRange(
                frame_hsv, self.yellow_dark, self.yellow_light)
            mask_red1 = cv2.inRange(frame_hsv, self.red_dark1, self.red_light1)
            mask_red2 = cv2.inRange(frame_hsv, self.red_dark2, self.red_light2)
            mask_red = cv2.add(mask_red1, mask_red2)

            self.draw(mask_blue, (255, 0, 0), 1, frame, "Azul")
            self.draw(mask_yellow, (0, 255, 255), 2, frame, "Amarillo")
            self.draw(mask_red, (0, 0, 255), 3, frame, "Rojo")

            self.photo = self.convert_frame_to_photo(frame)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        self.root.after(10, self.update)

    def draw(self, mask, color, id, frame, name):
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
                new_contour = cv2.convexHull(c)
                cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                cv2.putText(frame, str(name), (x + 10, y),
                            self.font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.drawContours(frame, [new_contour], 0, color, 3)

    def convert_frame_to_photo(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(image=img)
        return photo

    def quit_app(self):
        self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorTrackingApp(root)
    root.mainloop()
