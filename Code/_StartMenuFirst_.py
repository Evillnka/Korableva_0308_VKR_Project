from datetime import datetime
import tkinter as tk
from tkcalendar import Calendar

# импортируем классы и функции, определенные в defs
import _defs_


# объявление класса StartMenuFirst
# унаследованный от Frame
class StartMenuFirst(tk.Frame):
    # вызов метода init при создании объекта класса StartMenuFirst
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # объявление контроллера
        # служит для переключения между страницами
        self.controller = controller

        # установка в background изображения
        _defs_.setBackgroundImage(self, _defs_.getOneForAllBckgndPicture())
        # получения стандартных размеров кнопок
        buttonHeight, buttonWidth = _defs_.getStandartButtonSize()

        # установка даты на календарь
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        # объявление календаря
        calendar = Calendar(self, selectmode='day',year=year, month=month, day=day)

        # объявление виджета "кнопка" "Начать тренировку"
        # при нажатии на нее можно перейти на страницу StartMenuSecond
        nextPageButton = tk.Button(self, text="Начать тренировку", height= buttonHeight, width= buttonWidth,
                            command=lambda: controller.show_frame("StartMenuSecond"))

        # объявление виджета "кнопка" "Выход"
        # при нажатии на нее можно спровоцировать закрытие приложения
        quitButton = tk.Button(self, text = "Выход", height= buttonHeight, width= buttonWidth, command=self.quit)

        # укладка всех виджетов на фрейм
        calendar.pack(pady=50) # pack calendar into frame
        nextPageButton.pack(pady=30) # pack button into frame
        quitButton.pack(pady=10) # pack button into frame

