import tkinter as tk
from idlelib.tooltip import Hovertip

import logging

# импортирование пользовательских классов и функций из defs
import _defs_


# объявление класса ChangeTrainingPlan
# унаследованный от Frame
class ChangeTrainingPlan(tk.Frame):
    # вызов метода init при создании объекта класса ChangeTrainingPlan
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

        # установка размеров изображений (клторые будут в кнопках)
        imageHeight, imageWidth = 200, 300

        # количество нажатых кнопок
        self.selected = 0
        # кортеж, в котором будет храниться информация по кнопкам
        self.buttons = {}

        # создание фрейма, в котором будут располагаться кнопки
        internalFrame = tk.Frame(self, width=400, height=300)
        # расположение фрейма в ChangeTrainingPlan
        internalFrame.pack(pady = 30)

        i = 0
        j = 1
        # представление фрейма internalFrame как сетки для расположения кнопок
        # создается 3 строки и 5 столбцов (всего упражнений на выбор 6 штук)
        # расположим так, чтобы они оказались ровно по центру, а нижнюю дополнительную строку оставим под кнопку
        internalFrame.grid_rowconfigure(0, weight=1)
        internalFrame.grid_rowconfigure(1, weight=1)
        internalFrame.grid_rowconfigure(2, weight=1)
        internalFrame.grid_columnconfigure(0, weight=1)
        internalFrame.grid_columnconfigure(1, weight=1)
        internalFrame.grid_columnconfigure(2, weight=1)
        internalFrame.grid_columnconfigure(3, weight=1)
        internalFrame.grid_columnconfigure(4, weight=1)

        # расположение картинок в кнопки
        for yoga in self.yogaObject.getInternalYogaList():
            yogaImage = _defs_.getConvertedImage(_defs_.getStandartPath() + yoga + ".png", imageWidth, imageHeight)
            button = tk.Button(internalFrame, bg=_defs_.getWidgetColor(), image=yogaImage, height=imageHeight, width=imageWidth,
                                  compound=tk.CENTER, command=lambda name=yoga: self.buttonSelected(name))
            # кнопка с изображением асаны
            # изначально не нажата
            button.clicked = False
            # располагаем в сетке
            button.grid(row=i, column=j, sticky="nsew")

            # создание слоя под изображения
            canvas = tk.Canvas(internalFrame, width=imageWidth, height=imageHeight)
            canvas.imgtk = yogaImage
            canvas.create_image(0, 0, anchor=tk.NW, image=yogaImage)

            # сопоставим каждому упражнению кнопку
            self.buttons[yoga] = button

            # отслеживание параметров для сетки
            # при j > 3 - переход на новую строку
            if j<3:
                j += 1
            else:
                j = 1
                i += 1

        # изначально кнопка с переходом на страницу StartMenuSecond является неактивной
        # нужно выбрать хотя бы 4 упражнения для активации
        self.returnToTraining = tk.Button(self, text="Вернуться к тренировке", height=buttonHeight, width=buttonWidth,
                                          command=lambda: self.applyChanges(), state=tk.DISABLED)
        # создаие подсказки при наведении на кнопку
        tip_returnButton = Hovertip(self.returnToTraining, 'Выберите хотя бы 4 упражнения')
        self.returnToTraining.pack(pady = 20)


    # при нажатии на кнопку с упражнением вызывается метод buttonSelected
    # важно имя кнопки
    def buttonSelected(self, name):
        # вытаскиваем из кортежа кнопку, к которой только что обратились
        button = self.buttons[name]
        # если она не была еще нажата до этого
        if not button.clicked:
            # помечаем ее синей (выбранной)
            button.configure(bg="blue")
            # добавляем упражнение в список yogaObject
            self.yogaObject.appendElementToYoursYogaList(name)
            # увеличиваем количество выбранных кнопок на +1
            self.selected += 1
            # поменяем кнопку как нажатую
            button.clicked = True
        # если кнопка была уже нажата ранее
        else:
            # задний фон делаем белым
            button.configure(bg="white")
            # из списка в yogaObject удаляем запись об упражнении
            self.yogaObject.removeElementFromYoursYogaList(name)
            # уменьшаем количество выбранных кнопок на -1
            self.selected -= 1
            # помечаем как ненажатую
            button.clicked = False

        # если количество кнопок больше 4
        if self.selected >= 4:
            # делаем кнопку с возвращением назад активной
            self.returnToTraining.config(state=tk.NORMAL)
        # если нет
        else:
            # делаем кнопку с возвращением назад неактивной
            self.returnToTraining.config(state=tk.DISABLED)


    # метод, который сбрасывает состояние каждой кнопки в начальное
    # они не нажаты и не выбраны (фон белый)
    def initialButtons(self):
        #for names in _defs_.internalYogaList:
        for names in self.yogaObject.getInternalYogaList():
            button = self.buttons[names]
            button.clicked = False
            button.configure(bg="white")


    # initial elements before work with it
    # используется в момент обращения к данному фрейму
    def disableReturnButton(self):
        # update the yourYogaList
        self.yogaObject.clearYoursYogaList()

        # инициализируем используемые объекты
        self.selected = 0
        self.returnToTraining.config(state=tk.DISABLED)
        # инициализируем состояние каждой кнопки
        self.initialButtons()


    # метод, который необходимо вызвать перед переходом на следующий фрейм StartMenuSecond
    def applyChanges(self):
        # запись о изменении плана тренировки в журнал логирования
        logging.info("The training plan was changed")
        # сортировка элементов в списке упражнений для более простого обращения к ним
        self.yogaObject.sortList()
        # переход на фрейм StartMenuSecond
        self.controller.show_frame("StartMenuSecond")