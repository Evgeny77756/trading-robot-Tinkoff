from random import random
from tinkoff.invest import Quotation, OrderDirection, OrderType, Client
import Active
import creds
from Active import Active
from Active import TICKER, convert_Quontation


class SellActive(Active):

    def __init__(self, ticker):
        super().__init__(ticker)
        self.order_id = str(random())
        self.quantity = 1
        self.account_id = creds.id_test_account_all

    # продажа по рыночной цене
    def sell_market(self):
        with Client(creds.tok_test_all_accept) as client:
            r = client.orders.post_order(
                order_id=self.order_id,
                figi=self.figi,
                quantity=self.quantity,
                account_id=self.account_id,
                direction=OrderDirection.ORDER_DIRECTION_SELL,
                order_type=OrderType.ORDER_TYPE_MARKET
            )

        print('продажа при рыночной цене прошла успешно!')
        print(r)
        return r

    def sell_limit(self, sell_price):
        with Client(creds.tok_test_all_accept) as client:

            print('зашли в лимитку для продажи')
            print('цена на которую ставим лимитную заявку для продажу', sell_price)

            r = client.orders.post_order(
                order_id=self.order_id,
                figi=self.figi,
                quantity=self.quantity,
                price=sell_price,
                account_id=self.account_id,
                direction=OrderDirection.ORDER_DIRECTION_SELL,
                order_type=OrderType.ORDER_TYPE_LIMIT,
            )
        print('продажу при лимитной цене прошла успешно!')
        print(r)
        return r

    # получение цены для продажи актива
    # передаётся процент, который говорит, на сколько выше нужно продать актив,
    # относительно текущей цены
    def convert_sell(self, percent, current_price):

        # переводим из Quotation в float
        value = Active.convert_Quontation(current_price)
        value = value + (value * (percent / 100))

        # переводим из float в Quotation
        units = int(value)
        nano = int((value - units) * 100)
        nano *= 10 ** 7

        return Quotation(units=units, nano=nano)

    # меняем количество лотов для продажи актива
    def set_quantity(self, quantity):
        self.quantity = quantity

    # меняем рабочий аккаунт
    def set_account_id(self, account_id):
        self.account_id = account_id

