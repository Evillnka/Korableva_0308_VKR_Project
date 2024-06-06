import tkinter as tk
from tkinter import font as tkfont

# импортируем пользовательские классы
from _StartMenuFirst_ import StartMenuFirst
from _StartMenuSecond_ import StartMenuSecond
from _TrainingWaiting_ import TrainingWaiting
from _ChangeTrainingPlan_ import ChangeTrainingPlan
from _CheckCameraPerformance_ import CheckCameraPerformance
from _ResultTraining_ import  ResultTraining
from _TrainingRun_ import TrainingRun
from _StudyTraining_ import StudyTraining
from _ResultSheet_ import ResultSheet

import _defs_


# класс SampleApp, который является наследованным от Tk
# устанавливает параметры главного окна приложения
# вызывается из main при запуске
class SampleApp(tk.Tk):
    # метод вызывется при объявлении объекта класса
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # устанавливаем размеры окна
        width, height = _defs_.getAppSize()

        # устанавливаем название приложения
        self.title("App")
        self.geometry(str(width)+"x"+str(height))
        # правило: размеры окна менять нельзя
        self.resizable(0, 0)
        # нажатие клавиши Escape спровоцирует выход из программы
        self.bind('<Escape>', lambda e: self.quit())

        # установка иконки приложения
        self.tk.call("wm", "iconphoto", self._w, tk.PhotoImage(file=_defs_.getStandartPath()+"yoga"+_defs_.get_PNG()))

        # установка формата текста
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # контейнер — это место, куда мы поместим фреймы
        # друг на друга, затем тот, который мы хотим видеть
        # тот, что необходимо использовать, будет поднят над остальными
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # определение класса Камера
        self.cameraClass = _defs_.CameraUsage()
        # получение списка камер в системе
        self.cameraClass.printCameraNames()

        # определение всех страниц
        self.frames = {}
        for FrameTake in (StartMenuFirst, StartMenuSecond, TrainingWaiting,
                          ChangeTrainingPlan, CheckCameraPerformance, StudyTraining, TrainingRun, ResultTraining, ResultSheet):
            page_name = FrameTake.__name__
            frame = FrameTake(parent=container, controller=self)
            self.frames[page_name] = frame

            # поместить все страницы в одно место
            frame.grid(row=0, column=0, sticky="nsew")
        # поместить наверх страницу StartMenuFirst
        self.show_frame("StartMenuFirst")

    # при вызове метода show_frame() отразится та страница, название
    # которой ввели в page_name
    # вызов фрейма по его имени (если фрейм имеет уникальные функции,
    # которые необходимо вызвать до того, как к фрейму придется обратиться
    # -> надо написать «hassatr()»
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]

        # вызывается при открытии фрейма CheckCameraPerformance
        if hasattr(frame, 'findCameraCHECK'):
            frame.findCameraCHECK()

        # вызывается при открытии фрейма TrainingWaiting
        if hasattr(frame, 'on_show'):
            frame.on_show()

        # вызывается при открытии фрейма StudyTraining
        if hasattr(frame, 'findVideo'):
            frame.findVideo()

        # вызывается при открытии фрейма TrainingRun
        if hasattr(frame, 'poseCamera'):
            frame.poseCamera()

        # вызывается при открытии фрейма ChangeTrainingPlan
        if hasattr(frame, 'disableReturnButton'):
            frame.disableReturnButton()

        # вызывается при открытии фрейма ResultTraining
        if hasattr(frame, 'resultGet'):
            frame.resultGet()

        # вызывается при открытии фрейма ResultSheet
        if hasattr(frame, 'updateTable'):
            frame.updateTable()

        # "поднятие" фрейма
        frame.tkraise()
