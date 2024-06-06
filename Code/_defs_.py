import tkinter as tk
import cv2
import logging

import wmi

from PIL import Image, ImageTk

from gtts import gTTS
from pygame import mixer


# one object for all other classes
# Singleton pattern used!
class YOGAINFO:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(YOGAINFO, cls).__new__(cls)
            # object initial
            cls._instance.internalYogaList_xnames = [["yoga1", "Собака мордой вниз"],
            #cls._instance.internalYogaList_xnames = ["Собака мордой вниз",
                                                     ["yoga2", "Поза посоха на четырёх опорах"],
                                                     #"Поза посоха на четырёх опорах",
                                                     ["yoga3", "Поза стула"],
                                                     #"Поза стула",
                                                     ["yoga4", "Поза воина 2"],
                                                     #"Поза воина 2",
                                                     ["yoga5", "Поза треугольника"],
                                                     #"Поза треугольника",
                                                     ["yoga6", "Поза вытянутого угла"]]
                                                     #"Поза вытянутого угла"]
            #cls._instance.internalYogaList = ["yoga1", "yoga2", "yoga3", "yoga4", "yoga5", "yoga6"]
            cls._instance.standartYogaList = ["yoga1", "yoga2", "yoga3", "yoga4", "yoga5"]
            cls._instance.currentElement = 0
            cls._instance.yoursYogaList = cls._instance.standartYogaList
            cls._instance.yoursRecord = 0
            cls._instance.timeInTraining = 0
            cls._instance.turnOffComments = False
        return cls._instance

    def changeCommentsMode(self):
        self.turnOffComments = ~self.turnOffComments

    def setTimeInTraining(self, training_time):
        self.timeInTraining += training_time/60

    def initialTimeInTraining(self):
        self.timeInTraining = 0

    def getTimeInTraining(self):
        return self.timeInTraining

    def getCommentsMode(self):
        return self.turnOffComments

    def getStartedWithYogaList(self):
        self.currentElement = 0
        self.yoursRecord = 0
        # return yoursYogaList[currentElement]

    def getCurrentElementFromYoga(self):
        if (self.currentElement < len(self.yoursYogaList)):
            return self.yoursYogaList[self.currentElement]
        else:
            return "null"

    def setNextElementFromYogaList(self):
        self.currentElement += 1

    def sortList(self):
        self.yoursYogaList.sort()

    def getInternalYogaList(self):
        #return self.internalYogaList
        return (self.getColumnsFromList(0))

    def appendElementToYoursYogaList(self, elem):
        self.yoursYogaList.append(elem)

    def removeElementFromYoursYogaList(self, elem):
        self.yoursYogaList.remove(elem)

    def clearYoursYogaList(self):
        self.yoursYogaList.clear()

    def getYoursYogaListLen(self):
        return len(self.yoursYogaList)

    def getColumnsFromList(self, column_index):
        return [row[column_index] for row in self.internalYogaList_xnames]

    def getElementsName(self):
        #return self.internalYogaList_xnames[self.currentElement]
        return (self.getColumnsFromList(1))[self.currentElement]

    def searchInYogaList(self):
        names = []
        for row_a in self.yoursYogaList:
            for row_b in self.internalYogaList_xnames:
                if (row_a == row_b[0]):
                    names.append(row_b[1])

        return names

    def getAllNames(self):
        all_names = ',\n'.join(self.searchInYogaList())
        return all_names

    def setUsersRecord(self, recordValue):
        self.yoursRecord = recordValue
        #print(self.yoursRecord)

    def getUsersRecord(self):
        #print(self.yoursRecord)
        return self.yoursRecord


class CameraUsage:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CameraUsage, cls).__new__(cls)
            # object initial
            cls._instance.camera_as_device = cls._instance.get_cameras_wmi()
            cls._instance.cameras_number = cls._instance.set_cameras_number()
            cls._instance.camera_list = cls._instance.get_camera_list()
            cls._instance.camera_names = cls._instance.get_camera_names()
            cls._instance.selected_camera_id = cls._instance.getCameraID()
            cls._instance.not_working_cameras = 0

        return cls._instance

    def insert_mode(self):
        print("Min Camera ID OR Max Camera ID")
        print("Choice: ")


    def get_camera_list(self):
        null_handler = logging.NullHandler()
        logging.getLogger().addHandler(null_handler)

        camera_list = []

        for i in range(self.cameras_number):
            cap = cv2.VideoCapture(i)
            if cap is not None and cap.isOpened():
                #camera_list.append(i)
                camera_list.append([i, True])
                cap.release()
            else:
                logging.error("Cannot find camera with ID = " + str(i))
        return camera_list

    def get_cameras_wmi(self):
        wmi_obj = wmi.WMI()
        devices = wmi_obj.Win32_PnPEntity()
        camera_list = []

        for device in devices:
            if device.Name and 'camera' in device.Name.lower():
                camera_list.append(device)

        return camera_list

    def set_cameras_number(self):
        number = 0
        cameras = self.camera_as_device
        for _ in cameras:
            number += 1
        return number

    def get_camera_names(self):
        # Get camera list
        camera_names = ""

        cameras = self.camera_as_device
        for camera in cameras:
            if camera.Name and 'camera' in camera.Name.lower():
                camera_names += camera.Name + "; "
        logging.info("Founded cameras: " + camera_names)
        return camera_names

    def getCameraID(self):
        # 0 - built-in camera
        # 1 - web camera
        _camera_id = 0
        if self.camera_list:
            # connected to internal
            _camera_id = min(row[0] for row in self.camera_list)
            #_camera_id = min(self.camera_list, key=lambda x: x[0])
            #_camera_id = max(self.camera_list) #just testing
            logging.info(f"Selected camera ID: {_camera_id}")
        else:
            logging.info("Couldn't find any camera in device")

        return _camera_id

    def returnSelectedCameraID(self):
        return self.selected_camera_id - self.not_working_cameras
        # return self.selected_camera_id

    def printCameraNames(self):
        return self.camera_names

    # if camera's broken
    #def try_to_find_another_camera(self):
    #    if (self.selected_camera_id != self.cameras_number - 1):
    #    #if (self.selected_camera_id != 0):
    #        self.selected_camera_id += 1
    #        #self.selected_camera_id -= 1
    #    else:
    #        self.selected_camera_id = min(self.camera_list[0])
    #        #self.selected_camera_id = min(self.camera_list, key=lambda x: x[0])
    #        #self.selected_camera_id = max(self.camera_list)
    #    logging.info(f"Connected to camera with ID: {self.selected_camera_id}")

    def try_to_find_another_camera(self):
        # only called if camera is broken
        # цикл по всем найденным камерам (при первом запуске приложения)
        for i in range (self.cameras_number):
            # selected_camera_id - камера, которая использовалась до поломки
            # если камера с ID = selected_camera_id
            if self.camera_list[i][0] == self.selected_camera_id:
                # пометить камеру недоступной
                self.camera_list[i][1] = False
                # увеличить количество неработающих камер на 1
                self.not_working_cameras += 1
                # выход: все камеры перебирать не обязательно
                break

        print("Number of not working cameras: ", self.not_working_cameras)
        # объявление переменной cameraFound
        cameraFound = False
        # цикл по врем камерам
        for i in range (self.cameras_number):
            # если найдена камера у которой self.camera_list[i][1] = True
            # т.е. она рабочая
            if (self.camera_list[i][1]):
                # selected_camera_id берет ID рабочей камеры
                self.selected_camera_id = self.camera_list[i][0]
                # помечаем, что мы нашли камеру
                cameraFound = True
                # запись в лог о подключении к камере с другим ID
                logging.info(f"Connected to camera with ID: {self.selected_camera_id}")
                # выход: нам не нужно все перебирать (иначе запишется id самой последней камеры)
                break
        # если мы так и не нашли хотя бы одну рабочую камеру
        if not cameraFound:
            # установим selected_camera_id = -1, что будет значать провал в подключении
            # в тренировке это флаг о прекращении попыток поиска камер
            self.selected_camera_id = -1
            # запись в лог о провале в поиске рабочей камеры
            logging.error("Couldn't find any working camera")


def getOneForAllBckgndPicture():
    #return getConvertedImage(getStandartPath() + "frameImage" + get_PNG(), getAppSize()[0], getAppSize()[1])
    #return getConvertedImage(getStandartPath() + "frameImage1" + get_PNG(), getAppSize()[0], getAppSize()[1])
    return getConvertedImage(getStandartPath() + "frameImage2" + get_PNG(), getAppSize()[0], getAppSize()[1])


def getSpecialBckgndPicture():
    return getConvertedImage(getStandartPath() + "frameImage2_0" + get_PNG(), getAppSize()[0], getAppSize()[1])

def get_PNG():
    return ".png"


def get_MP4():
    return ".mp4"


def get_MP3():
    return ".mp3"


def get_DB():
    return ".db"


def setBackgroundImage(frame, frameimage):
    frame.configure(background="white")
    frame.background_image = frameimage
    frame.background_label = tk.Label(frame, image=frame.background_image)
    frame.background_label.place(x=0, y=0, relwidth=1, relheight=1)  # fullfill


def getConvertedImage(FILEPATH, width, height):
    photo = cv2.imread(FILEPATH)
    photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(photo, (width, height))))

    return imgtk


def getConvertedImageNo_W_H(FILEPATH):
    photo = cv2.imread(FILEPATH)
    photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(photo))

    return imgtk


def getStandartButtonSize():
    return 3, 35


def getAppSize():
    # width = 1280
    # height = 720
    return 1280, 720


def getWidgetColor():
    # d2fff1 - pink
    # ffdbdc - green
    # fffece - yellow
    return '#fffece'


def getStandartPath():
    # return "C:\\Users\\marin\\Downloads\\"
    return "S:\\VKR_FILES\\"


def create_gtts(language, text, path):
    _gtts_ = gTTS(text = text,
                  lang = language,
                  slow = False)

    _gtts_.save(path)


def play_sound(path):
    mixer.init()
    mixer.music.load(path)
    mixer.music.play()
