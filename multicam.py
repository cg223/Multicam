import tkinter as tk
from tkinter import ttk, Frame, CENTER, PhotoImage, Canvas
import cv2
from PIL import Image, ImageTk

class Window(tk.Tk):
    def __init__(self):
        #creates a tk.Tk instance and defines a number of class properties to store data
        super().__init__()
        self.cams = []
        self.currentFrame = 0
        self.frames = []
        self.numCams = 2
        self.camerasFrame = None
        
    def addCamera(self, index):
        #adds a camera input to the Window.cams list
        self.cams.append(cv2.VideoCapture(index, cv2.CAP_DSHOW))
        self.frames.append(None)
        
    def getFrame(self, index):
        #gets the current frame from a camera, and places it in the Window.frames list
        success, frame = self.cams[index].read()
        frame = cv2.cvtColor(frame, cv2.COLORBGR2RGB)
        PILframe = Image.fromarray(frame)
        self.frames[index] = PILframe
        
    def updateFrames(self):
        #for each camera, updates its frame in the Window.frames list.
        for i in range(len(self.cams)):
            self.getFrame(i)

    def setNumCams(self, num):
        self.numCams = num
        self.setLayout(num)

    def setLayout(self, num):
        match num:
            case "1":
                self.camerasFrame.rowconfigure(0, minsize=960, weight=960) #1: row 0 col 1
                self.camerasFrame.columnconfigure(0, minsize=112, weight=112)
                self.camerasFrame.columnconfigure(1, minsize=1706, weight=1706)
            case "2":
                self.camerasFrame.rowconfigure(0, minsize=210, weight=210) #1: row 1 col 0
                self.camerasFrame.rowconfigure(1, minsize=540, weight=540) #2: row 1 col 1
                self.camerasFrame.columnconfigure(0, minsize=960, weight=960)
                self.camerasFrame.columnconfigure(1, minsize=960, weight=960)


# for i in range(10):
#     success, _frame = cams[0].read()
#     _frame = cv2.cvtColor(_frame, cv2.COLOR_BGR2RGB)
#     PILframe = Image.fromarray(_frame)
#     currentFrame += 1
#     PILframe.save(f'images/frame{currentFrame}.jpeg')

#init fonts
spinFont = ("montserrat", 20)

#init root
root = Window()
root.geometry('1920x1040')
root.state('zoomed')
root['bg'] = '#2f2f2f'
root.title('The Magical Multicam')
root.iconphoto(False, PhotoImage(file='assets/MagicalMulticam.png'))
root.resizable(True, False)

#configure root
root.rowconfigure(0, minsize=80, weight=80) #topbar
root.rowconfigure(1, minsize=960, weight=960) #main
root.columnconfigure(0, weight=1) #main

#topbar
topBarFrame = Frame(root, bg='#1f1f1f', height=80, width=1920)
topBarFrame.grid(row=0, column=0)

#configure topbar
topBarFrame.rowconfigure(0, weight=80, minsize=80) #default
topBarFrame.columnconfigure(0, weight=20, minsize=20) #margin
topBarFrame.columnconfigure(1, weight=80, minsize=80) #logo
topBarFrame.columnconfigure(2, weight=1480, minsize=1480) #blank
topBarFrame.columnconfigure(3, weight=150, minsize=150) #number of cams spinbox
topBarFrame.columnconfigure(4, weight=20, minsize=20) #blank
topBarFrame.columnconfigure(5, weight=150, minsize=150) #cam setup button
topBarFrame.columnconfigure(6, weight=20, minsize=20) #margin

###topbar###
#logo
logoCanvas = Canvas(topBarFrame, bg="#1f1f1f", bd=0, highlightthickness=0)
logoCanvas.grid(row=0, column=1, sticky="NSEW")
logoImg = ImageTk.PhotoImage(Image.open("assets/MagicalMulticam.png").resize((80,80)).convert("RGBA"))
logoCanvas.create_image(40, 45, image=logoImg)

#numCams
numCams = tk.Spinbox(topBarFrame, from_=1, to=10, font=spinFont, bg="#2f2f2f", fg="#fefefe", justify="center", command=lambda: root.setNumCams(numCams.get()))
numCams.grid(row=0, column=3, sticky="NSEW")

#cameras frame
camerasFrame = Frame(root, bg="#111111", height=960, width=1920)
camerasFrame.grid(row=1, column=0)
root.camerasFrame = camerasFrame

#mainloop
root.mainloop()