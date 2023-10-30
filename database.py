import pymysql
from pymysql.err import OperationalError
from pymysql.err import InterfaceError


class DBConnection:

    def __init__(self, config: dict):    #передача конфигурационного файла в виде словаря
        self.config = config

    def __enter__(self):
        try:
            self.conn = pymysql.connect(**self.config)    # создание соединения с MySQL, мы посылаем словать (звезд распак)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            if err.args[0] == 1045:
                print('Неверный логин и пароль, повторите подключение')
                return None
            if err.args[0] == 2003:
                print('Неверно введен порт или хост для подключения к серверу')
                return None
            if err.args[0] == 1049:
                print('Такой базы данных не существует')
                return None
        except UnicodeEncodeError as err:
            print('Были введены символы на русском языке')
            return None
        except InterfaceError as err:
            print(err)
            return err

    def __exit__(self, exc_type, exc_value, exc_trace):
        if exc_value:
            if exc_value.args[0] == 'Курсор не был создан':
                print('Курсор не создан')
            elif exc_value.args[0] == 1064:
                print('Синтаксическая ошибка в запросе!')
                self.conn.commit()
                self.conn.close()
            elif exc_value.args[0] == 1146:
                print('Ошибка в запросе! Такой таблицы не существует.')
                self.conn.commit()
                self.conn.close()
            elif exc_value.args[0] == 1054:
                print('Ошибка в запросе! Такого поля не существует.')
                self.conn.commit()
                self.conn.close()
            exit(1)
        else:
            self.conn.commit()  # фиксация транзакции,изменение запроса
            self.cursor.close()
            self.conn.close()
            return True


def work_with_db(config: dict, sql: str) -> list:  #передача конфигурационного файла в виде словаря, функция для работы (открытия закрытия связи с бд)
    result = []
    with DBConnection(config) as cursor:   #объект класса config, вызывается метод init и enter
        cursor.execute(sql)    #взятие данных с помощью курсора
        # select name, email from ...
        schema = [column[0] for column in cursor.description]
        # schema = ['name','email']
        for item in cursor.fetchall():
            result.append(dict(zip(schema, item)))   #после этой строчки вызывается метод exit
    return result
