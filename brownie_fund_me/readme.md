# brownie not attach to GANACHE GUI automatically ???
Check that the port numbers are the same between GUI and CLI. 
Ganache (GUI) settings -> server and reset the port to 8545. Save and restart. Brownie should attach next time you run your deploy script.

# add brownie network
brownie networks add Ethereum ganache-local host=http://127.0.0.1:8545 chainid=1337
