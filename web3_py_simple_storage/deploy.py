from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

print("Installing...")
install_solc("0.8.7")
print("Installed done!")


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.7",
)

# print(compiled_sol)
with open("complied_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connect ganache chain =========================================================

# ----ENV NOTICE----CUSTOM FOR EACH ENVIRONMENT
# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# chain_id = 1337  # DEDAULT is 1337, NOT THE FUCKING THING show in GANACHE
# my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# private_key = os.getenv("GANACHE_AC1_PRIVATE_KEY") # never put privatekey in hard fixed code(or if u push to git, people will see it)


# ---rinkby---
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/f723aaebb5924d06ae4edb778db1862e"))
chain_id = 4 
my_address = "0x413CA9352303903cF022B69F270b14363EcaF608"
private_key = os.getenv("GANACHE_AC1_PRIVATE_KEY")

# ================================================================================

# Create contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print("nonce: ", nonce)

# 1. Build transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# 2. Sign transaction
signed_tranx = w3.eth.account.sign_transaction(transaction, private_key)

# 3. Send transaction
print("Deploying contract...")
send_tranx = w3.eth.send_raw_transaction(signed_tranx.rawTransaction)

# wait for response from blockchain
tranx_receipt = w3.eth.wait_for_transaction_receipt(send_tranx)

# Working with contract need:
# 1. Contract address
# 2. Contract abi
simple_storage = w3.eth.contract(address=tranx_receipt.contractAddress, abi=abi)


# Call(): SIMULATE making call and get return value
# Transact(): actually MAKE STATE CHANGE
# initial value of favorite number
print("retrieve() favorite number", simple_storage.functions.retrieve().call())

# create transaction
store_tranx = simple_storage.functions.store(8).buildTransaction({
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "from": my_address,
    "nonce": nonce + 1
})

sign_store_tranx = w3.eth.account.sign_transaction(store_tranx, private_key)
print("Updating contract...")
send_store_tranx = w3.eth.send_raw_transaction(sign_store_tranx.rawTransaction)
store_tranx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tranx)

print("Contract updated...")
print("retrieve() favorite number", simple_storage.functions.retrieve().call())

