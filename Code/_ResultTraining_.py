import tkinter as tk

import _defs_
from _DataBaseInfo_ import DataBaseInfo

import os


class ResultTraining(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.yogaObject = _defs_.YOGAINFO()
        self.db = DataBaseInfo()

        _defs_.setBackgroundImage(self, _defs_.getOneForAllBckgndPicture())

        buttonHeight, buttonWidth = _defs_.getStandartButtonSize()

        self.result = 0

        self.resultLabel = tk.Label(self, text="Ваш результат: " +  self.formateNumeric() + " %",
                               bg=_defs_.getWidgetColor())

        # initial button. Click to go page StartMenuFirst
        backToBeginningButton = tk.Button(self, text="Внести результаты в базу данных", height=buttonHeight, width=buttonWidth,
                                          command=lambda: controller.show_frame("ResultSheet"))

        self.resultLabel.pack(pady = 300)
        backToBeginningButton.pack(pady = 20)


    def play_result(self):
        if (self.result >= 75.0):
            path = _defs_.getStandartPath() + "win_result." + str(self.formateNumeric()) + _defs_.get_MP3()
        else:
            path = _defs_.getStandartPath() + "loose_result." + str(self.formateNumeric()) + _defs_.get_MP3()

        if not os.path.exists(path):
            if (self.result >= 75.0):
                _defs_.create_gtts("ru", "Поздравляем! Ваш результат равен " + str(self.result) + " %", path)
            else:
                _defs_.create_gtts("ru", "К сожалению, ваш результат равен " + str(self.result) +
                                   " %. Старайтесь упорнее и у Вас все получится!", path)

        _defs_.play_sound(path)

    def update_label(self):
        self.resultLabel.config(text="Ваш результат: " + self.formateNumeric() + " %")

    def formateNumeric(self):
        return "{:.1f}".format(self.result)

    def resultGet(self):
        self.result = self.yogaObject.getUsersRecord()
        self.db.insertNewRecord(self.yogaObject.getTimeInTraining(), self.yogaObject.getAllNames(), self.result)
        self.update_label()
        if not self.yogaObject.getCommentsMode():
            self.play_result()

