from brownie import FundMe, accounts, network, config, MockV3Aggregator
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVS = ["development", "ganache-local"]

# SINCE V3Aggregator v0.8 return 18 decimals
DECIMALS = 8 
DEFAULT_PRICE = 2000 * 10 ** 8

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    
def deploy_mock_v3_aggregator():
    print(f"The active network is ${network.show_active()}")
    print(f"Deploying Mocks...")
    
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, DEFAULT_PRICE, {"from": get_account()})
        
    print(f"Mocks Deployed!")
    