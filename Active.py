import time
from datetime import datetime, timedelta
from enum import Enum

from tinkoff.invest import Client, OrderDirection, OrderType, Quotation, InstrumentType, InstrumentIdType, \
    CandleInterval

import creds

TICKER = ["VKCO", "ALRS", "GAZP", "IRAO", "MTLR", "POLY", "RNFT", "TGKA", "YNDX"]
INTERVAL = []


# переводим Quotation во float
def convert_Quontation(quotation):
    value = list(quotation.__dict__.values())
    value[1] = int(value[1]/(10 ** 7))
    if value[1] < 10:
        value = str(value[0]) + '.0' + str(value[1])
    else:
        value = str(value[0]) + '.' + str(value[1])
    value = float(value)
    return value


# переводим из float в Quotation
def convert_float_in_Quotation(value):
    # переводим из float в Quotation
    units = int(value)
    nano = int((value - units) * 100)
    nano *= 10 ** 7

    return Quotation(units=units, nano=nano)


class Active:

    def __init__(self, ticker):
        self.ticker = ticker
        self.class_code = 'TQBR'
        self.figi = self.get_figi()
        self.price_step = self.get_price_step()
        self.lot = self.get_lot()
        self.interval = CandleInterval.CANDLE_INTERVAL_HOUR
        self.bids = self.current_price()[0]
        self.asks = self.current_price()[1]


    # получаем figi актива
    def get_figi(self):
        with Client(creds.tok_test_all_accept) as client:
            figi = client.instruments.get_instrument_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code='TQBR', id=self.ticker).instrument.figi
        return figi

    # текущий стакан
    def current_price(self):
        try:
            with Client(creds.tok_test_all_accept) as client:
                book = client.market_data.get_order_book(figi=self.figi, depth=50, instrument_id=self.figi)
                bids = book.bids
                asks = book.asks
            return bids, asks
        except Exception:
            print('Торги закрыты!')

    # меняем временной интервал
    def set_interval(self, interval):
        self.interval = interval

    # получаем лотность актива
    def get_lot(self):
        with Client(creds.tok_test_all_accept) as client:
            lot = client.instruments.get_instrument_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code='TQBR', id=self.ticker).instrument.lot
        return lot

    # шаг цены
    def get_price_step(self):
        with Client(creds.tok_test_all_accept) as client:
            price_step = client.instruments.get_instrument_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code='TQBR', id=self.ticker).instrument.min_price_increment
        return price_step

