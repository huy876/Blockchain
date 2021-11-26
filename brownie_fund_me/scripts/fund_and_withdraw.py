from brownie import FundMe
from brownie.network import account
from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVS, deploy_mock_v3_aggregator


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(fund_me.getPrice())
    print(entrance_fee)

def main():
    fund()