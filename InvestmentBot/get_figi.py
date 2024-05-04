import os
from pandas import DataFrame, read_json
from dotenv import load_dotenv
from tinkoff.invest import Client
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
from tinkoff.invest.grpc.instruments_pb2 import INSTRUMENT_STATUS_BASE


load_dotenv()
TOKEN = os.getenv("api_token")
ACC_ID = os.getenv('acc_id')


def get_shares(client_obj, tickers=None):
    if 'shares.json' not in os.listdir():
        shares_lst = client_obj.instruments.shares(instrument_status=INSTRUMENT_STATUS_BASE)
        df = DataFrame(shares_lst.instruments, columns=['ticker', 'name', 'figi', 'class_code'])
        if tickers:
            df = df[df['ticker'].isin(tickers)]
        df.to_json(path_or_buf='shares.json')


def read_shares_from_json(file_path='shares.json', tickers=None):
    df = read_json(file_path)
    return df if not tickers else df[df['ticker'].isin(tickers)]


if __name__ == "__main__":
    with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
        get_shares(client, tickers=("GAZP", "POLY", "AFKS", "SBER", "YNDX", "POSI"))
    print(read_shares_from_json(tickers=("GAZP", "POLY", "AFKS")))

