from brownie import accounts, config, SimpleStorage, network
import os

def deploy_simple_storage():
    account = getAccount()
    
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    transaction = simple_storage.store(8, {"from": account})
    transaction.wait(1) # how many block to wait
    updated_store_value = simple_storage.retrieve()
    print(updated_store_value)
    
def getAccount():
    if (network.show_active() == "development"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def main():
    deploy_simple_storage()