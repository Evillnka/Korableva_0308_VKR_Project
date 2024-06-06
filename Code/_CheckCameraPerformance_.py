import tkinter as tk

from PIL import Image, ImageTk
import cv2

import logging
import _defs_

import os


class CheckCameraPerformance(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.cameraClass = _defs_.CameraUsage()

        _defs_.setBackgroundImage(self, _defs_.getOneForAllBckgndPicture())
        buttonHeight, buttonWidth = _defs_.getStandartButtonSize()

        self.canvasWidth, self.canvasHeight = 500, 350

        yourCameraLabel = tk.Label(self, text="Ваша камера: ", bg=_defs_.getWidgetColor())

        returnButton = tk.Button(self, text="Вернуться к тренировке", height=buttonHeight, width=buttonWidth,
                                 command=lambda: self.returnToTraining())

        # Velocity difference caused with:
        # The built-in camera usually has direct access to system resources
        # and can be faster than an external webcam, which may require
        # additional initialization and communication time

        #self.cameraID = _defs_.getCameraID() --old
        self.cameraID = self.cameraClass.returnSelectedCameraID()

        #self.userCameraVideo = cv2.VideoCapture(cameraID)
        self.cameraCanvas = tk.Canvas(self, width=self.canvasWidth, height=self.canvasHeight)
        self.itsOkay = False
        self.successfuly_released = False

        self.okayLabel = tk.Label(self, text=" ", bg=_defs_.getWidgetColor())

        yourCameraLabel.pack(pady = 10)
        self.cameraCanvas.pack(pady = 20)
        self.okayLabel.pack(pady = 20)
        returnButton.pack(pady = 10)

        #self.showCamera()

    def findCameraCHECK(self):
        # camera catch
        self.cameraID = self.cameraClass.returnSelectedCameraID()
        self.successfuly_released = False
        self.userCameraVideo = cv2.VideoCapture(self.cameraID)
        self.itsOkay = False
        self.showCamera()

    def returnToTraining(self):
        if self.userCameraVideo is not None:
            self.successfuly_released = True
            self.userCameraVideo.release()
            #self.userCameraVideo = None

        self.controller.show_frame("StartMenuSecond")

    #def initCamera(self):
    #    self.itsOkay = False

    def play_audio(self, mode):
        if mode:
            path = _defs_.getStandartPath() + "camera_OK" + _defs_.get_MP3()
        else:
            path = _defs_.getStandartPath() + "camera_BR" + _defs_.get_MP3()

        if not os.path.exists(path):
            if mode:
                _defs_.create_gtts("ru", "Вас прекрасно видно! Так держать!", path)
            else:
                _defs_.create_gtts("ru",
                                   "К сожалению Вас не видит ни одна камера! "
                                   "Возможно, дело в драйверах системы. Обязательно перезапустите приложение!", path)

        _defs_.play_sound(path)

    def showCamera(self):
        ret, frame = self.userCameraVideo.read()
        if not ret:
            # only if is broken !
            if not self.successfuly_released:
                #current_camera_id = self.cameraID
                self.cameraClass.try_to_find_another_camera()
                self.cameraID = self.cameraClass.returnSelectedCameraID()
                #if (current_camera_id != self.cameraID):
                #    self.findCamera()
                if (self.cameraID != -1):
                    self.findCameraCHECK()
                else:
                    nocamera = _defs_.getConvertedImage(_defs_.getStandartPath() + "camera" + _defs_.get_PNG(), self.canvasWidth, self.canvasHeight)

                    self.cameraCanvas.imgtk = nocamera
                    self.cameraCanvas.create_image(0, 0, anchor=tk.NW, image=nocamera)

                    logging.error("Camera lost during it checking")

                    self.play_audio(False)
                    self.okayLabel.config(text="Мы Вас не видим!\nПроверьте камеру еще раз!")

                    return
            else:
                self.itsOkay = False
        else:
            if not self.itsOkay:
                self.itsOkay = True
                self.play_audio(True)
                self.okayLabel.config(text="Мы Вас отлично видим!")

            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.canvasWidth, self.canvasHeight))

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.cameraCanvas.imgtk = imgtk
            self.cameraCanvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

            self.update()
            self.after(10, self.showCamera)
