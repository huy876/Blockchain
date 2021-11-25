# brownie install
pip install eth-brownie

# init project
brownie init

# cmd
brownie compile
brownie run scripts/deploy.js

# save privatekey by brownie cmd
brownie accounts new <account name>         --- NOTE: add 0x before the private key
brownie accounts delete <account name>
brownie accounts list

# testing
brownie test
brownie test -k <function name>             --- test single function
brownie test -s                             --- more detail about test

# deploy to testnet
brownie networks list
brownie run scripts/deploy.py --network rinkeby

--- when deploy to a test net, brownie save contract to build/ deployment/4 (4 is id of rinkeby)

