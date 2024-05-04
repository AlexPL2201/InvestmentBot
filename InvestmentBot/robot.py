from tinkoff.invest import Client
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
from datetime import datetime, timedelta
from tinkoff.invest.grpc.marketdata_pb2 import CANDLE_INTERVAL_DAY

from get_figi import read_shares_from_json
from strategy import Analyzer
from account import Account


class Robot:
    def __init__(self, token: str, account: Account, ticker: str, strategy: Analyzer):
        self.token = token
        self.account = account
        self.strategy = strategy
        self.ticker = ticker
        self.instrument_info = read_shares_from_json(tickers=[self.ticker])

    def run_robot(self):
        with Client(self.token, target=INVEST_GRPC_API_SANDBOX) as client:
            candle = client.market_data.get_candles(
                figi=self.instrument_info['figi'].values[0],
                from_=datetime.now() - timedelta(days=15),
                to=datetime.now(),
                interval=CANDLE_INTERVAL_DAY,
            )
            sma_30 = self.strategy.analyze_candles(data=candle, window=3)

