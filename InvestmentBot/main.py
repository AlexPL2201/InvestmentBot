import os
from dotenv import load_dotenv

from robot import Robot
from account import AccountManager, Account
from strategy import SMAStrategy, Analyzer


load_dotenv()
TOKEN = os.getenv("api_token")
# ACC_ID = os.getenv('acc_id')
TICKERS = ("SBER",)


def main():
    accounts_mgr = AccountManager(token=TOKEN)
    account = Account(token=TOKEN, account=accounts_mgr.select_account())
    strategy = Analyzer(SMAStrategy())
    robot = Robot(token=TOKEN, account=account, ticker="SBER", strategy=strategy)
    robot.run_robot()


if __name__ == '__main__':
    main()
