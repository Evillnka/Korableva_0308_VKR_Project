import tkinter as tk
from  tkinter import ttk

import _defs_

from _DataBaseInfo_ import DataBaseInfo

class ResultSheet(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.yogaObject = _defs_.YOGAINFO()
        self.db = DataBaseInfo()

        _defs_.setBackgroundImage(self, _defs_.getOneForAllBckgndPicture())

        buttonHeight, buttonWidth = _defs_.getStandartButtonSize()

        columns = self.db.get_columns()

        style = ttk.Style()
        style.theme_use("clam")
        style.configure('Treeview', rowheight=90, font=('Helvetica', 11))

        self.tableWithResults = ttk.Treeview(self, columns=columns, show="headings")

        for column in columns:
            self.tableWithResults.column(column, anchor=tk.CENTER)
            self.tableWithResults.heading(column, text=column)

        # initial button. Click to go page StartMenuFirst
        backToBeginningButton = tk.Button(self, text="Закончить тренировку", height=buttonHeight, width=buttonWidth,
                                          command=lambda: self.returnToMenu())

        backToBeginningButton.pack(side = tk.BOTTOM, pady = 30)
        self.tableWithResults.pack(side = tk.TOP, pady = 60)

    def returnToMenu(self):
        self.controller.show_frame("StartMenuFirst")

    def updateTable(self):
        self.tableWithResults.delete(*self.tableWithResults.get_children())

        records = self.db.getAllRecords()
        tag = "COLOR"
        for index, record in enumerate(records):
            if (index != 0):
                tag = "NOCOLOR"
            self.tableWithResults.insert("", "end", values=record, tags=tag)
            #self.tableWithResults.insert("", "end", values=record)
        self.tableWithResults.tag_configure('COLOR', background='lightpink')


