import time
from datetime import datetime
from random import random
from tinkoff.invest import Quotation, OrderDirection, OrderType, Client, CandleInterval
import creds
import math
from BuyActive import BuyActive
from Active import TICKER, convert_Quontation, Active, convert_float_in_Quotation
from DataBase import TableDB, DataBase, TypeColumn, AmountSymbForVarchar
from SellActive import SellActive

###### ТАБЛИЦЫ В БД #######

TABLE_FOR_LOTS = 'table_lots'   # таблица для статичных значений стратегии
BUY_STOCKS = 'buy_stocks'       # таблица для динамических значений цен покупок и продаж актива

############ ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ДЛЯ НАСТРОЙКИ #############

PROFIT_PERCENTAGE = 0.1                 # процент для прибыли
BUY_COMISSION = 0.3                     # комиссия за покупку
SELL_COMISSION = 0.3                    # комиссия за продажу

PERCENT_TO_BUY_1_LOT = 1                # процент, который указывает на сколько цена покупки 1го должна быть ниже указанной
PERCENT_TO_BUY_2_LOT = 1                # процент, который указывает на сколько цена покупки 2го должна быть ниже указанной
PERCENT_TO_BUY_3_LOT = 0.1                # процент, который указывает на сколько цена покупки 3го должна быть ниже указанной
PERCENT_TO_BUY_4_LOT = 0.1                # процент, который указывает на сколько цена покупки 4го должна быть ниже указанной

WORKING_ASSET = TICKER[4]               # выбираем рабочий актив
total_active = 548.17                   # общее количество денег в колонке
parts_in_columns = 4                    # количество частей на которое делится колонка
INTERVAL_FOR_BUY = CandleInterval.\
    CANDLE_INTERVAL_15_MIN              # рабочий временной интервал для покупки
active = Active(WORKING_ASSET)          # базовый объект рабочего актива
active_buy = BuyActive(WORKING_ASSET)   # объект рабочего актива для покупки
active_sell = SellActive(WORKING_ASSET) # объект рабочего актива для продажи
TOTAL_COMISSION = PROFIT_PERCENTAGE + BUY_COMISSION + SELL_COMISSION        # общая сумма для сделки с учётом комиссии за покупку или продажу

######### ПОДКЛЮЧЕНИЕ БД И ТАБЛИЦ ########

db = DataBase('localhost', 'root', '', 'tinkoffrobot')
db.create_connection()
dbTable = TableDB(db.connection, f'{BUY_STOCKS}')                       # соединение с таблицей активов
staticData = TableDB(db.connection, f'{TABLE_FOR_LOTS}')                # соединение со статичной таблицей


# функция для получения и заполнения данными таблицы с динамическими ценами для покупок и продаж актива в БД
def update_buy_stocks(obj_active):

    # вычисляем максимальную цену текущего дня
    with Client(creds.tok_test_all_accept) as client:
        now = datetime.now()
        prices = client.get_all_candles(figi=obj_active.figi, from_=datetime(now.year, now.month, now.day), to=now, interval=INTERVAL_FOR_BUY)
        mass_prices = []
        for price in prices:
            mass_prices.append(convert_Quontation(price.high))
        max_price_at_day = max(mass_prices)
        print(max_price_at_day)

        # узнаём, какие мои лоты уже куплены, и какой мой лот нужно будет покупать
        lst_price_buy = []
        next_buy = None         # следующий лот для покупки
        r = None
        orderus = None
        for i in range(1, 5):
            x = dbTable.select_column('price_buy', condition_column='id', condition_value=i)
            if x[0][0] is None:
                next_buy = i
                print(next_buy)
                break
            lst_price_buy.append(x)

        # если это первая покупка моего лота
        if next_buy == 1:
            price_to_buy = convert_float_in_Quotation(max_price_at_day)
            print('максимальная цена за день: ', price_to_buy)
            price_to_buy = active_buy.convert_buy(PERCENT_TO_BUY_1_LOT, price_to_buy)
            r = active_buy.buy_limit(price_to_buy)
            print(r)
            # заносим идентифмкатор в базу данных, чтобы по нему потом узнавать информацию
            user_order = r.order_id
            print(user_order)
            dbTable.update_column('order_id', f'{user_order}', 'id', 1)
            orderus = dbTable.select_column('order_id', 'id', 1)
            print(orderus)
            mass_orders = client.orders.get_orders(account_id=creds.id_test_account_all)

            # ищем информацию о нужном ордере
            for i in mass_orders.orders:
                print(i.order_id)
                if int(i.order_id) == orderus[0][0]:
                    print('order_id: ', i.order_id)
                    print(i.initial_order_price)
                    print(i.executed_order_price)
                    break
            else:
                print('Нет такого ордера в портфеле!')
            # breakpoint()

        # если это вторая покупка моего лота
        elif next_buy == 2:
            price_to_buy = dbTable.select_column('price_buy', condition_column='id', condition_value=1)[0][0]
            print(price_to_buy)

            price_to_buy = convert_float_in_Quotation(price_to_buy)
            print('цена, купленная в первом моём лоте: ', price_to_buy)
            price_to_buy = active_buy.convert_buy(PERCENT_TO_BUY_2_LOT, price_to_buy)
            r = active_buy.buy_limit(price_to_buy)
            # print(r)

            # заносим идентифмкатор в базу данных, чтобы по нему потом узнавать информацию
            user_order = r.order_id
            print(user_order)
            dbTable.update_column('order_id', f'{user_order}', 'id', 2)
            orderus = dbTable.select_column('order_id', 'id', 2)
            print(orderus)
            mass_orders = client.orders.get_orders(account_id=creds.id_test_account_all)

            breakpoint()
            # ищем информацию о нужном ордере
            for i in mass_orders.orders:
                print(i.order_id)
                if int(i.order_id) == orderus[0][0]:
                    print('order_id: ', i.order_id)
                    print(i.initial_order_price)
                    break
            else:
                print('Нет такого ордера в портфеле!')

        elif next_buy == 3:

            # если это вторая покупка моего лота
            if next_buy == 3:
                try:
                    price_to_buy = convert_float_in_Quotation(
                        dbTable.select_column('price_buy', condition_column='id', condition_value=3))
                    print('цена, купленная в первом моём лоте: ', price_to_buy)
                    price_to_buy = active_buy.convert_buy(PERCENT_TO_BUY_3_LOT, price_to_buy)
                    r = active_buy.buy_limit(price_to_buy)
                    # print(r)

                    # заносим идентифмкатор в базу данных, чтобы по нему потом узнавать информацию
                    user_order = r.order_id
                    print(user_order)
                    dbTable.update_column('order_id', f'{user_order}', 'id', 3)
                    orderus = dbTable.select_column('order_id', 'id', 3)
                    print(orderus)
                    mass_orders = client.orders.get_orders(account_id=creds.id_test_account_all)

                    # ищем информацию о нужном ордере
                    for i in mass_orders.orders:
                        print(i.order_id)
                        if int(i.order_id) == orderus[0][0]:
                            print('order_id: ', i.order_id)
                            print(i.initial_order_price)
                            break
                    else:
                        print('Нет такого ордера в портфеле!')

                except:
                    print('Что то пошло не так...')

        elif next_buy == 4:

            # если это вторая покупка моего лота
            if next_buy == 4:
                try:
                    price_to_buy = convert_float_in_Quotation(
                        dbTable.select_column('price_buy', condition_column='id', condition_value=4))
                    print('цена, купленная в первом моём лоте: ', price_to_buy)
                    price_to_buy = active_buy.convert_buy(PERCENT_TO_BUY_4_LOT, price_to_buy)
                    r = active_buy.buy_limit(price_to_buy)
                    # print(r)

                    # заносим идентифмкатор в базу данных, чтобы по нему потом узнавать информацию
                    user_order = r.order_id
                    print(user_order)
                    dbTable.update_column('order_id', f'{user_order}', 'id', 4)
                    orderus = dbTable.select_column('order_id', 'id', 4)
                    print(orderus)
                    mass_orders = client.orders.get_orders(account_id=creds.id_test_account_all)

                    # ищем информацию о нужном ордере
                    for i in mass_orders.orders:
                        print(i.order_id)
                        if int(i.order_id) == orderus[0][0]:
                            print('order_id: ', i.order_id)
                            print(i.initial_order_price)
                            break
                    else:
                        print('Нет такого ордера в портфеле!')

                except:
                    print('Что то пошло не так...')

        # цикл пока не будет куплен актив
        while True:
            # постоянно проверяем статус ордера для заявки на продажу
            rr = client.orders.get_order_state(account_id=creds.id_test_account_all,
                                               order_id=r.order_id).execution_report_status.value
            print('статус: ', rr)
            print(Quotation(units=r.initial_order_price.units, nano=r.initial_order_price.nano))
            print('информация об ордере: ', r)
            if rr == 1:
                # заносим цену покупку в БД
                time.sleep(3)

                mass_orders = client.orders.get_orders(account_id=creds.id_test_account_all)
                print(mass_orders)
                price_limit_order = None
                # ищем информацию о нужном ордере
                for i in mass_orders.orders:
                    print(i.order_id)
                    if int(i.order_id) == orderus[0][0]:
                        print('order_id: ', i.order_id)
                        print(i.initial_order_price)
                        print(i.executed_order_price)
                        price_limit_order = i.executed_order_price
                        break
                else:
                    print('Нет такого ордера в портфеле!')

                print('заходим в БД..')
                # price_limit_order = convert_Quontation(Quotation(units=r.executed_order_price.units, nano=r.executed_order_price.nano))
                print(price_limit_order)
                price_limit_order = convert_Quontation(price_limit_order)
                dbTable.update_column('price_buy', f'{price_limit_order}', 'id', 1)
                dbTable.update_column('amount_lots', f'{r.lots_executed}', 'id', 1)
                dbTable.update_column('current_profit', f'{0}', 'id', 1)
                dbTable.update_column('deposite_money', f'{price_limit_order * r.lots_executed}', 'id', 1)
                dbTable.update_column('current_money', f'{0}', 'id', 1)
                price_to_buy_2_lot = convert_float_in_Quotation(price_limit_order)
                price_to_buy_2_lot = active_buy.convert_buy(PERCENT_TO_BUY_2_LOT, price_to_buy_2_lot)
                price_to_buy_2_lot = convert_Quontation(price_to_buy_2_lot)
                dbTable.update_column('price_next_buy', f'{price_to_buy_2_lot}', 'id', 1)

                break

            active_change = Active(WORKING_ASSET)
            quontation_price_buy = Quotation(units=r.executed_order_price.units, nano=r.executed_order_price.nano)
            print('limit order: ', convert_Quontation(quontation_price_buy), 'current price for buy: ', convert_Quontation(active_change.bids[0].price))

            time.sleep(1)

        print('исполненная цена', r.executed_order_price)






# функция для получения и заполнения данными таблицы с лотами в БД
def update_table_lots(obj, obj_active):
    try:
        amount_lots = math.ceil(total_active / convert_Quontation(obj_active.bids[0].price) * obj_active.lot)
    except Exception:
        print('Торги закрыты!')
        amount_lots = 0
        return amount_lots
    obj.update_column('name_active', f'"{WORKING_ASSET}"')
    obj.update_column('total_active', f'{total_active}')
    obj.update_column('parts_in_columns', f'{parts_in_columns}')
    obj.update_column('lots_in_part', f'{math.ceil(amount_lots / parts_in_columns)}')
    obj.update_column('amount_lots', f'{amount_lots}')
    obj.update_column('lot_active', f'{obj_active.lot}')

    name_active_user = obj.select_column('name_active')[0][0]               # название актива
    total_active_user = obj.select_column('total_active')[0][0]             # количество денег в колонке
    parts_in_columns_user = obj.select_column('parts_in_columns')[0][0]     # количество частей, на которое делится колонка
    lots_in_part_user = obj.select_column('lots_in_part')[0][0]             # количество лотов в колонке
    amount_lots_user = obj.select_column('amount_lots')[0][0]               # общее количество лотов в колонке
    lot_active_user = obj.select_column('lot_active')[0][0]                 # лотность актива

    return name_active_user, total_active_user, parts_in_columns_user, lots_in_part_user, amount_lots_user, lot_active_user


info = update_table_lots(staticData, active)
print(info)

# col = '*'
# res = dbTable.select_column(col, condition_column='id', condition_value=3)
# print(res)

update_buy_stocks(dbTable, active)