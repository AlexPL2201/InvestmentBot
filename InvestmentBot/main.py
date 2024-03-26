import os
from dotenv import load_dotenv
from tinkoff.invest import Client
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX

load_dotenv()
TOKEN = os.getenv("api_token")


def connect_to_sandbox():
    with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
        print(client.users.get_accounts())


if __name__ == '__main__':
    connect_to_sandbox()
