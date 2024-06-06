import tkinter as tk

import _defs_
from _DataBaseInfo_ import DataBaseInfo

import os


class TrainingWaiting(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.yogaObject = _defs_.YOGAINFO()

        _defs_.setBackgroundImage(self, _defs_.getOneForAllBckgndPicture())
        buttonHeight, buttonWidth = _defs_.getStandartButtonSize()

        self.canvasWidth, self.canvasHeight = 500, 350

        nextTrainingLabel = tk.Label(self, text="Следующее упражнение:", bg=_defs_.getWidgetColor())

        self.yogaPicture = _defs_.getConvertedImage(_defs_.getStandartPath() + self.yogaObject.getCurrentElementFromYoga() + _defs_.get_PNG(), self.canvasWidth, self.canvasHeight)

        self.photoCanvas = tk.Canvas(self, width=self.canvasWidth, height=self.canvasHeight)
        self.photoCanvas.imgtk = self.yogaPicture
        self.photoCanvas.create_image(0, 0, anchor=tk.NW, image=self.yogaPicture)

        self.MAX_TIME = 20
        transpPicture = _defs_.getConvertedImage(_defs_.getStandartPath() + "border" + ".png", 300, 120)
        #transpPicture = _defs_.getConvertedImageNo_W_H("S:\\VKR_FILES\\" + "border" + _defs_.get_PNG())
        self.timeLabel = tk.Label(self, text="Осталось времени: " + str(self.MAX_TIME), bg=_defs_.getWidgetColor())
        #self.timeLabel = tk.Label(self, text="Осталось времени: " + str(self.MAX_TIME), image=transpPicture)

        self.remainingTime = self.MAX_TIME
        self.stopTimer = True

        canvasWidth = _defs_.getAppSize()[0]
        skipTrainingCanvas = tk.Canvas(self, highlightthickness=0, bg=_defs_.getWidgetColor(), width=canvasWidth,
                                    height=buttonHeight)
        skipThisTrainingButton = tk.Button(skipTrainingCanvas, text="Пропустить упражнение",  height= buttonHeight, width= buttonWidth,
                                           command=lambda: self.nextExersize())
        skipThisTrainingButton.pack(side=tk.RIGHT, pady = 30)

        showTrialButton = tk.Button(self, text="Посмотреть TRIAL",  height= buttonHeight, width= buttonWidth,
                           command=lambda: self.reviewExersize())

        skipTimerCanvas = tk.Canvas(self, highlightthickness=0, bg = _defs_.getWidgetColor(), width=canvasWidth, height=buttonHeight)
        skipTimerButton = tk.Button(skipTimerCanvas, text="Начать сразу!", height=buttonHeight, width=buttonWidth,
                                    command=lambda: self.startNow())
        skipTimerButton.pack(side=tk.LEFT, padx = 80, pady = 30)

        skipTrainingCanvas.pack(fill="x", side=tk.TOP)
        skipTimerCanvas.pack(fill="x", side=tk.BOTTOM)
        nextTrainingLabel.pack(side=tk.TOP)
        self.photoCanvas.pack(side=tk.TOP)
        self.timeLabel.pack(side=tk.LEFT, padx=150, pady=10)
        showTrialButton.pack(side=tk.RIGHT, padx=150, pady=10)


    def update_label(self):
        self.timeLabel.config(text="Осталось времени: " + str(self.remainingTime))

    def play_timer(self):
        path = _defs_.getStandartPath() + "timer" + str(self.remainingTime) + _defs_.get_MP3()

        if not os.path.exists(path):
            _defs_.create_gtts("ru", str(self.remainingTime), path)

        _defs_.play_sound(path)

    def timer(self):
        if not self.stopTimer:
            if self.remainingTime > 0:
                self.remainingTime -= 1
                self.update_label()
                if not self.yogaObject.getCommentsMode() and self.remainingTime in (0, 1, 2, 3):
                    self.play_timer()
                self.timer_id = self.after(1000, self.timer)
            else:
                self.controller.show_frame("TrainingRun")


    def startNow(self):
        self.remainingTime = 0


    # refactor the image
    def imageRefator(self):
        self.yogaPicture = _defs_.getConvertedImage(_defs_.getStandartPath() + self.yogaObject.getCurrentElementFromYoga() + _defs_.get_PNG(), self.canvasWidth, self.canvasHeight)

        self.photoCanvas.imgtk = self.yogaPicture
        self.photoCanvas.create_image(0, 0, anchor=tk.NW, image=self.yogaPicture)

        self.update()


    def nextExersize(self):
        self.stop_timer()

        if hasattr(self, 'timer_id'):  # Check if the timer ID exists
            self.after_cancel(self.timer_id)  # Cancel the timer

        self.yogaObject.setNextElementFromYogaList()

        if (self.yogaObject.getCurrentElementFromYoga() != "null"):
            #self.controller.show_frame("TrainingWaiting")
            self.on_show()
        else:
            db = DataBaseInfo()
            db.set_DATETIME_END()
            self.controller.show_frame("ResultTraining")

    def play_asana_name(self):
        yoga_name = self.yogaObject.getElementsName()
        path = _defs_.getStandartPath() + str(yoga_name) + _defs_.get_MP3()

        if not os.path.exists(path):
            _defs_.create_gtts("ru", "Следующее упражнение " + yoga_name, path)

        _defs_.play_sound(path)

    # initial the frame
    def on_show(self):
        self.imageRefator()
        if not self.yogaObject.getCommentsMode():
            self.play_asana_name()

        self.remainingTime = self.MAX_TIME
        self.start_timer()
        self.timer()

    def  stop_timer(self): self.stopTimer = True

    def start_timer(self): self.stopTimer = False

    def reviewExersize(self):
        self.stop_timer()
        if hasattr(self, 'timer_id'):  # Check if the timer ID exists
            self.after_cancel(self.timer_id)  # Cancel the timer

        self.controller.show_frame("StudyTraining")


