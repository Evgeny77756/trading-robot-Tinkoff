from random import random
from tinkoff.invest import Quotation, OrderDirection, OrderType, Client
import Active
import creds
from Active import Active
from Active import TICKER, convert_Quontation


class BuyActive(Active):

    def __init__(self, ticker):
        super().__init__(ticker)
        self.order_id = str(random())
        self.quantity = 1
        self.account_id = creds.id_test_account_all

    # покупка по рыночной цене
    def buy_market(self):
        with Client(creds.tok_test_all_accept) as client:
            r = client.orders.post_order(
                order_id=self.order_id,
                figi=self.figi,
                quantity=self.quantity,
                account_id=self.account_id,
                direction=OrderDirection.ORDER_DIRECTION_BUY,
                order_type=OrderType.ORDER_TYPE_MARKET
            )

        print('покупка при рыночной цене прошла успешно!')
        print(r)
        return r

    def buy_limit(self, buy_price):
        with Client(creds.tok_test_all_accept) as client:

            print('зашли в лимитку для покупки')
            print('цена на которую ставим лимитную заявку для покупки', buy_price)

            r = client.orders.post_order(
                order_id=self.order_id,
                figi=self.figi,
                quantity=self.quantity,
                price=buy_price,
                account_id=self.account_id,
                direction=OrderDirection.ORDER_DIRECTION_BUY,
                order_type=OrderType.ORDER_TYPE_LIMIT,
            )
        print('покупка при лимитной цене прошла успешно!')
        print(r)
        return r

    # получение цены для покупки актива
    # передаётся процент, который говорит, на сколько ниже нужно купить актив,
    # относительно текущей цены
    def convert_buy(self, percent, current_price):

        # переводим из Quotation в float
        value = convert_Quontation(current_price)
        value = value - (value * (percent / 100))

        # переводим из float в Quotation
        units = int(value)
        nano = int((value - units) * 100)
        nano *= 10 ** 7

        return Quotation(units=units, nano=nano)

    # меняем количество лотов для покупки актива
    def set_quantity(self, quantity):
        self.quantity = quantity

    # меняем рабочий аккаунт
    def set_account_id(self, account_id):
        self.account_id = account_id

#
# buy = BuyActive(TICKER[1])
# print(buy.__dict__)
# print(buy.account_id)
# buy.set_account_id(creds.id_broker_account_all)
# print(buy.account_id)
# print(convert_Quontation(buy.price_step))