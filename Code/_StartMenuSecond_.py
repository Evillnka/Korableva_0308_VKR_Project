import tkinter as tk
from tkinter.messagebox import showinfo

# импортирование пользовательских классов и функций из defs
# и DataBaseInfo
import _defs_
from _DataBaseInfo_ import DataBaseInfo


# объявление класса StartMenuSecond
# унаследованный от Frame
class StartMenuSecond(tk.Frame):
    # вызов метода init при создании объекта класса StartMenuSecond
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # объявление контроллера
        # служит для переключения между страницами
        self.controller = controller

        # объявление объекта класса YOGAINFO, который имеет паттерн Singleton
        # т.е. экземпляр класса создается один на все последующие объявления
        self.yogaObject = _defs_.YOGAINFO()

        # установка в background изображения
        _defs_.setBackgroundImage(self, _defs_.getOneForAllBckgndPicture())
        # получения стандартных размеров кнопок
        buttonHeight, buttonWidth = _defs_.getStandartButtonSize()

        # initial button. Click to go page TrainingWaiting
        startTrainingButton = tk.Button(self, text="Начать", height= buttonHeight, width= buttonWidth,
                           command=lambda: self.getStarted())

        # initial button. Click to go page ChangeTrainingPlan
        changePlanButton = tk.Button(self, text="Изменить план тренировки", height= buttonHeight, width= buttonWidth,
                           command=lambda: controller.show_frame("ChangeTrainingPlan"))

        # initial button. Click to go page CheckCameraPerformance
        checkCameraPerformaceButton = tk.Button(self, text="Проверить работоспособность камеры", height= buttonHeight, width= buttonWidth,
                           command=lambda: controller.show_frame("CheckCameraPerformance"))

        # initial button. Click to turn off the comments
        self.turnOffComments = tk.Button(self, text="Выключить комментарии", height= buttonHeight, width= buttonWidth,
                                    command=lambda: self.turnOff())

        # initial button. Click to go page StartMenuFirst
        backToBeginningButton = tk.Button(self, text="Вернуться в начало", height= buttonHeight, width= buttonWidth,
                           command=lambda: controller.show_frame("StartMenuFirst"))

        # упаковка всех виджетов на странице
        startTrainingButton.pack(pady = 60)
        changePlanButton.pack(pady = 10)
        checkCameraPerformaceButton.pack(pady = 10)
        self.turnOffComments.pack(pady = 10)
        backToBeginningButton.pack(pady = 60)

    # метод, в котором озвучиваются действия, связанные с кнопкой "Отключить/Включить комментарии"
    def play_voice(self, mode):
        # обращение к месту, где лежит запись
        path = _defs_.getStandartPath() + "voice_" + str(mode) + _defs_.get_MP3()

        # mode = True - при выключении комментариев
        # mode = False - при включении
        if mode:
            _defs_.create_gtts("ru", "Хорошо, не буду Вам мешать! Если что, обращайтесь!", path)
        else:
            _defs_.create_gtts("ru", "Спасибо, всегда буду рада Вам помочь!", path)
        # вызов функции, озвучивающей изменения с кнопкой по пути к файлу
        _defs_.play_sound(path)

    # метод, в котором отображается реакция программы на изменение состояния
    # кнопки "Отключить/Включить комментарии"
    def turnOff(self):
        # запомнить, что кнопка выключена (чтобы вся программа знала, что озвучивать комментарии не надо)
        self.yogaObject.changeCommentsMode()
        offMode = self.yogaObject.getCommentsMode()
        # вызов метода play_voice
        self.play_voice(offMode)
        # замена конфигурации кнопки Отключить/Включить комментарии" в зависимости от того,
        # нужно ли чтобы комментарии были озвучены или нет
        if offMode:
            self.turnOffComments.config(text="Включить комментарии")
        else:
            self.turnOffComments.config(text="Выключить комментарии")

    # метод, который срабатывает при нажатии на кнопку "Начат тренировку"
    def getStarted(self):
        # установка порядкового номера упражнений в 0
        # инициализация записи о тренировке
        self.yogaObject.getStartedWithYogaList()
        # объявление объекта класса DataBaseInfo который имеет паттерн Singleton
        # т.е. экземпляр класса создается один на все последующие объявления
        db = DataBaseInfo()
        # вызов метода set_DATETIME_START, который записывает время начала тренировки
        db.set_DATETIME_START()
        # вызов метода initialTimeInTraining, который устанавливает время, проведенное
        # в тренировке в 0
        self.yogaObject.initialTimeInTraining()
        # открытие фрейма TrainingWaiting
        self.controller.show_frame("TrainingWaiting")



