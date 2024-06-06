# импортирование пользовательских классов из соответствующих скриптов
from _ShowApp_ import SampleApp
from _DataBaseInfo_ import DataBaseInfo

import logging
import sys
import signal


# обработчик сигнала для принудительного завершения программы
def signal_handler(signal, frame):
    # запись в журнал логирования ошибки KeyboardInterrupt
    logging.error("KeyboardInterrupt detected!")
    logging.info("App is forced to close")
    # закрытие приложения с кодом 0 (успешное завершение программы)
    sys.exit(0)


# точка входа в программу
if __name__ == '__main__':
    # настройка записи в журнал логирования “logger.log”
    logging.basicConfig(level=logging.INFO, filename="logger.log", filemode="a",
                        format="%(asctime)s %(levelname)s %(message)s")
    # первые записи в журнал логирования
    logging.info('-' * 50)  # separator
    logging.info("App is opened")

    # установка обработчика SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    # создание объекта класса DataBaseInfo (пользовательский класс)
    db = DataBaseInfo()
    # открытие соединения с базой данных
    db.openConnection()

    # создание экземпляра класса SampleApp (пользовательский класс)
    app = SampleApp()
    # метод, отслеживающий интерактивность компонентов приложения
    app.mainloop()

    # закрытие соединение с базой данных
    db.closeConnection()
    # запись в лог информации об успешном закрытии приложения
    logging.info("App is normally closed")
