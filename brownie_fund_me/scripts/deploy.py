from brownie import FundMe, accounts, network, config, MockV3Aggregator
from scripts.utils import get_account, deploy_mock_v3_aggregator, LOCAL_BLOCKCHAIN_ENVS
import os
from web3 import Web3

def deploy_fund_me():
    account = get_account()
    
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mock_v3_aggregator()            
        price_feed_address = MockV3Aggregator[-1].address;
        
    fund_me = FundMe.deploy(price_feed_address, {"from": account}, publish_source=config["networks"][network.show_active()]["verify"]) #publish_source=true allow view more detail on etherScan/ contract tab
    print(f"Contract deployed to {fund_me.address}")

def main():
    deploy_fund_me();