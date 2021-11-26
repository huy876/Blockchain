from brownie import FundMe, accounts, network, config
from scripts.utils import getAccount
import os

def deploy_fund_me():
    account = getAccount()
    
    if network.show_active() != "development":
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        print(f"The active network is ${network.show_active()}")
        print(f"Deploying Mocks...")    
        
    fund_me = FundMe.deploy(price_feed_address, {"from": account}, publish_source=True) #publish_source=true allow view more detail on etherScan/ contract tab
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me();