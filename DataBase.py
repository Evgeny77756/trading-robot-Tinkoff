import mysql.connector
from mysql.connector import Error
from enum import Enum


class TypeColumn(Enum):

    int = 'INT'
    varchar = 'VARCHAR'
    double = 'DOUBLE'
    null = 'NULL'
    not_null = 'NOT NULL'
    int_auto_increment = 'INT AUTO_INCREMENT PRIMARY KEY'

class AmountSymbForVarchar(Enum):
    amount10 = '(10)'
    amount50 = '(50)'
    amount100 = '(100)'
    amount200 = '(200)'
    amount255 = '(255)'


class TableDB:

    def __init__(self, db_name, table_name, columns=None):
        self.db_name = db_name
        self.table_name = table_name
        self.columns = columns
        self.lst_name_columns = []
        self.lst_type_columns = []
        self.cursor = db_name.cursor()

    # создание таблицы в базе данных
    def create_table(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({self.columns})")

    # добавление записи в базу данных
    def insert_data(self, new_values, namesUser=None):
        names = namesUser
        if names is None:
            for name in self.get_name_columns():
                names += f"{name}, "
            names = names[:-2]
        self.cursor.execute(f'INSERT INTO {self.table_name} ({names}) '
                            f'VALUES ({new_values});')
        self.db_name.commit()

    # добавление колонки в таблицу
    def add_column(self, new_column, value, amount_for_varchar='(255)'):
        if new_column in self.get_name_columns():
            print('Такая колонка уже существует!!!')
        else:
            new_column += ' ' + value + amount_for_varchar
            self.cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN  {new_column};")
            self.db_name.commit()

    # выбор колонки из таблицы
    def select_column(self, column, condition_column='id', condition_value=1):
        if condition_column is None:
            self.cursor.execute(f"SELECT {column} FROM {self.table_name};")
            result = self.cursor.fetchall()
            return result
        else:
            self.cursor.execute(f"SELECT {column} FROM {self.table_name} "
                                f"WHERE {condition_column} = {condition_value};")
            result = self.cursor.fetchall()
            return result

    # изменение записи в базе данных
    def update_column(self, column_name, new_value, condition_column='id', condition_value=1):
        self.cursor.execute(f"UPDATE {self.table_name} "
                            f"SET {column_name} = {new_value} "
                            f"WHERE {condition_column} = {condition_value};")
        self.db_name.commit()

    # убираем дубликаты в таблице по столбцам
    def distinct_unique(self, columns):
        self.cursor.execute(f"DELETE t1 FROM {self.table_name} t1 "
                            f"JOIN {self.table_name} t2 "
                            f"WHERE t1.id > t2.id "
                            f"AND t1.{columns} = t2.{columns};")
        self.db_name.commit()

    # получить данные о колонках таблицы
    def get_column(self):
        self.cursor.execute(f"SHOW COLUMNS FROM {self.table_name};")
        columns = self.cursor.fetchall()

        return columns

    # список названий колонок
    def get_name_columns(self):
        self.lst_name_columns = []
        for col in self.get_column():
            self.lst_name_columns.append(col[0])

        return self.lst_name_columns

    # список типов колонок
    def get_type_columns(self):
        self.lst_type_columns = []
        for col in self.get_column():
            self.lst_type_columns.append(col[1])

        return self.lst_type_columns


# База данных пользователя
class DataBase:
    def __init__(self, host_name, user_name, user_password, db_name):
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.db_name = db_name
        self.connection = None

    # подключение к базе данных
    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.user_password,
                database=self.db_name
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return self.connection



