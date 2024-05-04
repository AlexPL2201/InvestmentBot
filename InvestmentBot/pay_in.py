import os
from dotenv import load_dotenv
from tinkoff.invest import Client, MoneyValue
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX

load_dotenv()
TOKEN = os.getenv('api_token')
ACC_ID = os.getenv('acc_id')


def pay_in_account(client_obj, acc_id, amount, currency='rub'):
    client_obj.sandbox.sandbox_pay_in(
        account_id=acc_id,
        amount=MoneyValue(currency=currency, units=amount)
    )
    print(client_obj.operations.get_portfolio(account_id=acc_id).total_amount_currencies)


if __name__ == '__main__':
    with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
        pay_in_account(client_obj=client, acc_id=ACC_ID, amount=100000)
