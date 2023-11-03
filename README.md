# trading-robot-Tinkoff

Создаём файл .env
в этом файле будут храниться секретные токены, которые потом подставляем в 
файл creds.py

# creds.py
Необходимые библиотеки:

    tinkoff-investments


- Регистрируемся в личном кабинете в Тинькофф инвестициях.
- Создаём токен общего доступа.
- Записываем токен в переменную tok_test_all_accept, которая находится в файле .env
    Этот токен будет рабочим.
- И записываем переменную id_broker_account_all
    Этот токен будет запасным

Пример:
tok_broker_all_accept = 'YOUR TOKEN'
tok_test_all_accept = 'YOUR TOKEN'

- Далее получаем id для каждого из токенов и записываем их в переменные:
    id_broker_account_all - id для запасного токена
    id_test_account_all - id для тестового токена

###################################################################################
# Active.py

    Необходимые библиотеки:
    
        tinkoff-investments
    
    
    Описание: 
    В этом модуле находится class Active.
    В этом классе находится вся необходимая информация о рабочем инструменте.
    
    ########### ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ################
    
    TICKER - список тикеров инструментов, с которыми мы планируем работать
    INTERVAL - диапазон для отслеживания инструментов (интервал графика)
    
    ########### ФУНКЦИИ МОДУЛЯ ################
    def convert_Quontation(quotation) - функция для перевода формата Quontation во float
    
    def convert_float_in_Quotation(value) - перевод float в Quontation

# class Active

    хранящиеся данные в классе: 
    
        self.ticker - тикер инструмента 
        self.class_code - для тикера класс код
        self.figi - фиги инструмента
        self.price_step - шаг цены у инструмента
        self.lot - лотность инструмента
        self.interval - свечной интервал графика у инструмента
        self.bids - цены для покупки в текущем стакане
        self.asks - цены для продажи в текущем стакане

    МЕТОДЫ: 
        
        def get_figi(self)
            Получаем figi инструмента 
            Получаемый тип str

        def current_price(self)
            Получаем текущий стакан инструмента
            Получаемый тип Quontation

        def set_inteval(self, interval)
            При необходимости меняем свечной интервал инструмента
            У переменной interval значение должно быть типа CandleInterval.

        def get_lot(self)
            Получаем лотность инструмента
            Получаемый тип int

        def get_price_step(self)
            Получаем шаг цены
            Получаемый тип Quontation
            

        def get_price_step(self)
            Получаем шаг цены инструмента
            Получаемый тип Quontation

####################################################################################
# DataBase.py

    Модуль содержит классы и данные для работы с БД

    - Устанавливаем библиотеку mysql-connector-python
        1. Подключение к БД MySQL
        2. Выполнение запроса на создание БД MySQL

    - Подключаем библиотеки 
        import mysql.connector

# class TableDB - класс для создания таблицы БД

    хранящиеся данные в классе: 

        self.db_name            - название БД в которой мы создаём таблицу
        self.table_name         - название создаваемой таблицы
        self.columns            - название колонок и через пробел их тип
        self.lst_name_columns   - список названий колонок
        self.lst_type_columns   - список названий типов колонок
        self.cursor             - курсор БД        

    принимает при инициализации:
        
        db_name             - название БД
        table_name          - название таблицы
        columns = None      - колонки таблицы, которые будут записаны
                            в таблицу при её создании. 
                            По умолчанию в ней не будет колонок

    Методы класса

        def create_table(self) 
            Создание таблицы в БД
        
        def insert_data(self, new_column, value, nameUsers = None)
            Добавляем в таблицу запись

        def add_column(self, new_column, value, amount_for_varchar = '(255)')
            Добавление колонки в таблицу

        def select_column(self, column, condition_column = 'id', condition_value = 1)
            Выбор колонки из таблицы с заданным 'id'

        def update_column(self, column_name, new_value, condition_column = 'id', condition_value = 1)
            Изменение записи в БД

        def distinct_unique(self, column)
            Убираем дубликаты в таблице

        def get_column(self) 
            Получаем данные о колонках таблицы

        def get_name_columns(self)
            Получаем названия колонок

        def get_type_columns(self)
            Получаем типы колонок

# BuyActive.py

    Модуль содержит класс BuyActive(), который создаёт различные заявки для покупки актива

    Подключаем модуль Active.py

# class BuyActive() - класс наследуется от класса class Active()
    
    хранящиеся данные в классе: 
    
    self.super()            - наследует данные от класса Active()
    self.order              - строковый тип (рандом)
    self.quantity           - количество покупаемых активов

    принимает при инициализации:

    ticker                  - тикер актива

    Методы класса

        def buy_market(self) 
            создаём рыночную заявку для покупки актива
        
        def buy_limit(self, buy_price)
            создаём лимитную заявку для покупки актива

            buy_limit - цена, при которой выставляем заявку

        def convert_buy(self, percent, current_price)
            Прибавляет к цене, при которой купили актив, процент прибавки

            percent - процент прибавки для цены актива, при которой нужно будет продать актив
            current_price - цена, при которой мы купили актив

        def set_quantity(self, quantity)
            Меняет количество лотов у покупаемых активов

            quantity - получаем новое значение для количества покупаемых активов

        def set_account_id(self, account_id)
            Меняет рабочий аккаунт
    
            account_id - новый аккаунт



# SellActive.py

    Модуль содержит класс SellActive(), который создаёт различные заявки для продажи актива

    Подключаем модуль Active.py

# class SellActive(Active) - аналогично class BuyActive(self), описанного выше