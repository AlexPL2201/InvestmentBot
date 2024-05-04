from termcolor import colored
from tinkoff.invest import Client, MoneyValue
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX


class AccountManager:
    def __init__(self, token: str):
        self.token = token
        self.accounts = self._get_user_accounts()

    def _get_user_accounts(self):
        with Client(self.token, target=INVEST_GRPC_API_SANDBOX) as client:
            accounts = client.users.get_accounts().accounts
            if not accounts:
                raise Exception(colored("No accounts found.", 'white', 'on_red'))
            return accounts

    def select_account(self):
        while True:
            try:
                print("List of found accounts:")
                for i, account in enumerate(self.accounts):
                    print(f"\t{i}. Account's ID: {account.id} (Name: {account.name})")
                index = int(input(colored("Enter account code: ", 'green')))
                if len(self.accounts) > index >= 0:
                    return self.accounts[index]
                raise ValueError
            except ValueError:
                print(colored("\nInvalid input. Please try again.\n", 'white', 'on_red'))


class Account:
    def __init__(self, token, account):
        self.account = account
        self.portfolio = self.get_portfolio_by_id(account_id=account.id, token=token)

    def get_portfolio_by_id(self, account_id, token):
        with Client(token, target=INVEST_GRPC_API_SANDBOX) as client:
            pf = client.operations.get_portfolio(account_id=account_id)
            if pf.total_amount_currencies.units == 0:
                self.pay_in_account(client_obj=client, acc_id=account_id, amount=100000)
            return pf

    @staticmethod
    def pay_in_account(client_obj, acc_id, amount, currency='rub'):
        client_obj.sandbox.sandbox_pay_in(
            account_id=acc_id,
            amount=MoneyValue(currency=currency, units=amount)
        )