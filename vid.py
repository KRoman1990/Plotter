import subprocess
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import sys
import os

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width * 2, height = self.vid.height+20)
        self.canvas.pack()

        # Button that lets the user start a print
        self.btn_print=tkinter.Button(window, text="Print", width=50, command=self.print)
        self.btn_print.pack(anchor=tkinter.CENTER, expand=True)

        # Sign to gray image and svg format-like image
        self.sign_gray=tkinter.Label(window, text="Gray image",)
        self.sign_black_white=tkinter.Label(window, text="SVG-like image (Inverted)",)
        self.canvas.create_window(self.vid.width/2, 10, window=self.sign_gray)
        self.canvas.create_window(self.vid.width*1.5, 10, window=self.sign_black_white)
       
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()
        
    def print(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            faces = faceCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
            for (x, y, w, h) in faces:
                crop_img = frame[y:y+h, x:x+w]
            w = crop_img.shape[1] * 10
            h = crop_img.shape[0] * 10
            size = (w, h)
            crop_img = cv2.resize(crop_img, size)
            path = r'D:\Users\roman\potrace-1.16.win64'
            cv2.imwrite(os.path.join(path, 'image.bmp'), crop_img)
            subprocess.call([path+'\PlotterStart.bat'])
            

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        if ret:
            faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            faces = faceCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
            for (x, y, w, h) in faces:
                 cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            thresh, black_white_image = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
            self.photo_gray = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.photo_black_white = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(black_white_image))
            self.canvas.create_image(0, 20, image = self.photo_gray, anchor = tkinter.NW)
            self.canvas.create_image(self.vid.width, 20, image = self.photo_black_white, anchor = tkinter.NW)
        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")
