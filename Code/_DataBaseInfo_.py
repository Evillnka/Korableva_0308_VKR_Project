import sqlite3
from datetime import datetime

import logging

import _defs_


class DataBaseInfo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataBaseInfo, cls).__new__(cls)
            # object initial
            cls._instance.connection = None
            cls._instance.cursor = None
            cls._instance.database_name = "results_db"
            cls._instance.table_name = "RESULTS"
            cls._instance.notConnected = False
            cls._instance.DATETIME_START = None
            cls._instance.DATETIME_END = None
        return cls._instance

    def closeConnection(self):
        self.connection.close()
        logging.info("Successfully closed the connection with DB " + "'" + self.database_name + "'")

    # метод открытия соединения с БД
    def openConnection(self):
        # установление соединения с субд SQLite
        self.connection = sqlite3.connect(_defs_.getStandartPath()+self.database_name+_defs_.get_DB())
        try:
            # создание курсора, с помощью которого будут осуществляться запросы к бд
            self.cursor = self.connection.cursor()
            # запись в лог об успешном подключении к бд
            logging.info("Successfully connected to the DB " + "'" + self.database_name + "'")
            # используется для проверки наличия таблиц в данной бд
            self.checkTheTables()
        except Exception as ex:
            # при неудавшейся попытке подключения к бд - закрываем соединение
            self.closeConnection()
            # запись в лог о неудачной попытке соединения
            logging.error("Cannot set the connection with DB " + "'" + self.database_name + "'")

    # проверка наличия целевой таблицы
    def checkTheTables(self):
        # запрос на получение названий таблиц из БД
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # запись результата запроса сохраняем в tables
        tables = self.cursor.fetchall()
        for table in tables:
            # если среди всех таблиц есть "RESULTS"
            if (table[0] == self.table_name):
                # выход
                return
        # если нет такой таблицы - создаем ее в методе createTable
        self.createTable()

    # создание таблицы RESULTS в случае ее отсутствия
    def createTable(self):
        # emergency solution
        # использование объекта курсор для написания sql запроса направленного на создание
        # таблицы RESULTS с колонками: RECORD_ID, DATETIME_START, DATETIME_END, TRAINING_TIME, EXERCISES, RESULT
        self.cursor.execute(" CREATE TABLE IF NOT EXISTS " + self.table_name + """ (
                                RECORD_ID   INTEGER UNIQUE,
                                DATETIME_START    TEXT NOT NULL,
                                DATETIME_END    TEXT NOT NULL,
                                TRAINING_TIME REAL NOT NULL,
                                EXERCISES	TEXT NOT NULL,
                                RESULT  	REAL NOT NULL,
                                PRIMARY KEY(RECORD_ID AUTOINCREMENT)); """)
        # сохранение изменений в бд
        self.connection.commit()
        # запись в лог об успешном создании таблицы RESULTS
        logging.info("Successfully created table " + self.table_name + " in DB " + "'" + self.database_name + "'")

    # получение последних 5 записей в таблице RESULTS
    def getAllRecords(self):
        # выполнение команды SELECT
        self.cursor.execute("SELECT " + ', '.join(self.get_columns()) + " FROM " + self.table_name
                            + " ORDER BY " + "RECORD_ID" + " DESC LIMIT 5")
        # возвращение результата в виде списка записей
        return self.cursor.fetchall()

    def get_columns(self):
        self.cursor.execute("PRAGMA table_info(" + self.table_name + ")")
        columns = self.cursor.fetchall()

        column_names = [column[1] for column in columns]
        column_names.pop(0)

        return column_names

    def returnInsertValuesFormat(self, valuesList):
        string = "("
        for value in valuesList:
            string += str(value)
            if (value != valuesList[-1]):
                string += ", "
        string += "),"
        return string

    def get_date_string(self):
        return "%d.%m.%Y %H:%M"

    def set_DATETIME_START(self):
        now = datetime.now()
        self.DATETIME_START = now.strftime(self.get_date_string())

    def set_DATETIME_END(self):
        now = datetime.now()
        self.DATETIME_END = now.strftime(self.get_date_string())

    # занесение в таблицу RESULTS информации о проведенной тренировке
    # входные данные: train - время, затраченное на тренировку
    # ex - список упражнений, которые были в этой тренировке
    # res - процент выполнени всех упражнений
    def insertNewRecord(self, train, ex, res):
        # формирование списка с информацией о тренировке
        valuesList = (self.DATETIME_START, self.DATETIME_END, train, ex, res)
        # выполнение команды INSERT INTO
        self.cursor.execute("INSERT INTO " + self.table_name +
                            " (DATETIME_START, DATETIME_END, TRAINING_TIME, EXERCISES, RESULT) VALUES (?, ?, ?, ?, ?)",
                            valuesList)
        # сохранение изменений в таблице
        self.connection.commit()
