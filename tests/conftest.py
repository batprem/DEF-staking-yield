import pytest
from web3 import Web3
from brownie import network, MockERC20
from scripts.helpful_script import get_account


@pytest.fixture
def ACTIVE_NETWORK():
    return network.show_active()


@pytest.fixture
def account():
    return get_account()


@pytest.fixture
def amount_staked():
    return Web3.toWei(1, "ether")


@pytest.fixture
def random_erc20():
    account = get_account()
    erc20 = MockERC20.deploy({"from": account})
    return erc20
