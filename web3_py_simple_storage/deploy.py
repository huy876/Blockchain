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

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connect ganache chain =========================================================

# ----ENV NOTICE----CUSTOM FOR EACH ENVIRONMENT
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337 # DEDAULT is 1337, NOT THE FUCKING THING show in GANACHE
my_address = "0x42E614D0c63b1Cd3e437d52220531d960F5f5382"

# ----ENV NOTICE----NEED TO ADD Ox to front of PRIVATE KEY when copy from ganache
# NEVER HARD CODE PRIVATE KEY, if push to git hub, some one can see and steal
# private_key = "0x041591028e191378a79191a6f7d3757991f2794783ab271cdbc0f02847d44910"
private_key = os.getenv("GANACHE_AC1_PRIVATE_KEY")

# ================================================================================

# Create contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

#1. Build transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
#2. Sign transaction
signed_tranx = w3.eth.account.sign_transaction(transaction, private_key)

#3. Send transaction
tranx_hash = w3.eth.send_raw_transaction(signed_tranx.rawTransaction)

# wait for response from blockchain
# tranx_receipt = w3.eth.wait_for_transaction_receipt(tranx_hash)