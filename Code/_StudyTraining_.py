import tkinter as tk
from PIL import Image, ImageTk
import cv2

from pygame import mixer

import _defs_


class StudyTraining(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.yogaObject = _defs_.YOGAINFO()

        _defs_.setBackgroundImage(self, _defs_.getOneForAllBckgndPicture())
        buttonHeight, buttonWidth = _defs_.getStandartButtonSize()

        self.canvasWidth, self.canvasHeight = 500, 350

        self.videoCanvas = tk.Canvas(self, width=self.canvasWidth, height=self.canvasHeight)
        returnButton = tk.Button(self, text="Вернуться к тренировке", height=buttonHeight, width=buttonWidth,
                                 command=lambda: self.returnToTraining())

        repeatVideoButton = tk.Button(self, text="Повторить видео", height=buttonHeight, width=buttonWidth,
                                 command=lambda: self.repeatVideo())

        self.videoCanvas.pack(pady=20)
        #returnButton.pack(anchor="nw", padx=400, pady=30)
        returnButton.pack(side=tk.LEFT, padx=150, pady=10)
        repeatVideoButton.pack(side=tk.RIGHT, padx=150, pady=10)


    def repeatVideo(self):
        if self.yogaVideo is not None:
            self.play_audio()
            self.yogaVideo.release()
            self.yogaVideo = cv2.VideoCapture(self.videoPATH)
            #self.yogaVideo.set(cv2.CAP_PROP_POS_FRAMES, 0)


    def displayVideo(self):
        ret, frame = self.yogaVideo.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.canvasWidth, self.canvasHeight))

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.videoCanvas.imgtk = imgtk
            self.videoCanvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

        self.update()
        self.after(30, self.displayVideo)

    def play_audio(self):
        mixer.init()
        # mixer.music.load(getStandartPath()+"yoga5.mp3")
        mixer.music.load(_defs_.getStandartPath()+self.yogaObject.getCurrentElementFromYoga()+_defs_.get_MP3())
        mixer.music.play()


    def findVideo(self):
        # camera catch
        # self.videoPATH = _defs_.getStandartPath()+"yoga5.mp4"
        self.videoPATH = _defs_.getStandartPath()+self.yogaObject.getCurrentElementFromYoga()+_defs_.get_MP4()
        self.yogaVideo = cv2.VideoCapture(self.videoPATH)

        self.play_audio()

        self.displayVideo()

    def returnToTraining(self):
        if self.yogaVideo is not None:
            mixer.music.stop()
            self.yogaVideo.release()
            # self.userCameraVideo = None

        self.controller.show_frame("TrainingWaiting")