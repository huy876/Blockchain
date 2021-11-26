from brownie import FundMe, accounts, network, config

def getAccount():
    if (network.show_active() == "development"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])