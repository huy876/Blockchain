from solcx import compile_standard, install_solc

import json

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
