from brownie import SimpleStorage, accounts

def test_deploy():
    # Arranging
    account = accounts[0]
    # Acting
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    # Assert
    assert starting_value == expected
    
def test_update():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act
    simple_storage.store(8, {"from": account}).wait(1) # wait 1 block complete
    expected = 8  
    # Assert     
    assert expected == simple_storage.retrieve()
