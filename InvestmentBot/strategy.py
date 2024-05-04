import abc

import pandas as pd
from tinkoff.invest.schemas import GetCandlesResponse, Quotation


class Indicator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def calculate(self, data: GetCandlesResponse, window: int):
        pass


class Analyzer:
    def __init__(self, strategy: Indicator):
        self.__strategy = strategy

    def set_strategy(self, strategy: Indicator):
        self.__strategy = strategy

    def analyze_candles(self, data: GetCandlesResponse, window: int):
        self.__strategy.calculate(data, window)


class SMAStrategy(Indicator):
    def calculate(self, data: GetCandlesResponse, window: int):
        df = pd.DataFrame(data.candles[0:15])
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        print(df)
        for i, candle in enumerate(data.candles):
            sma: Quotation = Quotation(0, 0)
            sma_int = 0
            try:
                for j in range(i, i + window):
                    sma += data.candles[j].close
                sma_int = (sma.units + sma.nano / pow(10, 9)) / window
                print(f'SMA{window} ({candle.time} - {data.candles[i + window - 1].time}) = {sma_int}')
            except IndexError:
                break


class EMAStrategy(Indicator):
    def calculate(self, data: GetCandlesResponse, window: int):
        print('EMA strategy')
