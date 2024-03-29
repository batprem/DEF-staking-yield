import brownie
from brownie import (
    accounts,
    config,
    network,
    MockV3Aggregator,
    Contract,
    VRFCoordinatorMock,
    LinkToken,
    interface,
    MockDAI,
    MockWETH,
)
from web3 import Web3


OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "ganache-local-2"]


DECIMALS = 18
INITIAL_PRICE_FEED_VALUE = 2e21
BREED_MAPPING = ["PUG", "SHIBA_INU", "ST_BERNARD"]


def get_account(index=None, account_id=None):
    active_network = network.show_active()
    if index:
        return accounts[index]
    if account_id:
        return accounts.load(account_id)
    if (
        active_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or active_network in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallet"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "dai_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
    "fau_token": MockDAI,
    "weth_token": MockWETH,
}


def get_contract(contract_name):
    """
    This function will grab the contract address from the brownie config

    Args:
        contract_name (string)
    Returns:
        brownie.network.contract.ProjectContract
    """
    active_network = network.show_active()
    contract_type = contract_to_mock[contract_name]
    if active_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # Note that Local networks do not contain chain link contract address by default
        # we need to monk them up
        if len(contract_type) <= 0:
            # Get the latest deployed contract, deploy one if doesn't exist
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][active_network][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_PRICE_FEED_VALUE):
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = get_account()
    print("Deploying Mock Link Token...")
    link_token = LinkToken.deploy({"from": account})
    print("Deploying Mock Price Feed...")
    mock_price_feed = MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account}
    )
    print(f"Deployed to {mock_price_feed.address}")
    print("Deploying Mock DAI...")
    dai_token = MockDAI.deploy({"from": account})
    print(f"Deployed to {dai_token.address}")
    print("Deploying Mock WETH")
    weth_token = MockWETH.deploy({"from": account})
    print(f"Deployed to {weth_token.address}")


def fund_contract_with_link(
    contract_address: str,
    account: brownie.network.account.Account = None,
    link_token: Contract = None,
    amount: int = 0.1e18,
):
    """
    Contract which call external API need link token for request
    As a result, we first need to fund contract with link token
    """
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # tx = link_token.transfer(contract_address, amount, {"from", amount})
    link_token_contract = interface.LinkTokenInterface(link_token.address)
    link_token_contract.transfer(contract_address, amount, {"from": account})
    print("Fund contract")


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]
