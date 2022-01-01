from brownie import network, exceptions, MockERC20
from scripts.helpful_script import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    INITIAL_PRICE_FEED_VALUE,
    get_account,
    get_contract,
    DECIMALS,
)
from scripts import deploy
from scripts.deploy import deploy_token_farm_dapp_token, KEPT_BALANCE
import pytest
from web3 import Web3
from tests.conftest import ACTIVE_NETWORK, account, amount_staked, random_erc20


def test_set_price_feed_contract(ACTIVE_NETWORK, account):
    # Arrange
    deploy.ACTIVE_NETWORK = ACTIVE_NETWORK
    if ACTIVE_NETWORK not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    print(f"Working on {ACTIVE_NETWORK}")
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_dapp_token()

    # Act
    price_feed_address = get_contract("eth_usd_price_feed")
    token_farm.setPriceFeedContract(
        dapp_token.address, price_feed_address, {"from": account}
    )

    # Assert
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == price_feed_address
    with pytest.raises(exceptions.VirtualMachineError):
        # Call by non owner
        token_farm.setPriceFeedContract(
            dapp_token.address, price_feed_address, {"from": non_owner}
        )
    return token_farm, dapp_token


def test_stake_tokens(ACTIVE_NETWORK, account, amount_staked):
    # Arrange
    deploy.ACTIVE_NETWORK = ACTIVE_NETWORK
    if ACTIVE_NETWORK not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # token_farm, dapp_token = deploy_token_farm_dapp_token()
    deploy.ACTIVE_NETWORK = ACTIVE_NETWORK
    if ACTIVE_NETWORK not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    print(f"Working on {ACTIVE_NETWORK}")
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_dapp_token()

    # Act
    price_feed_address = get_contract("eth_usd_price_feed")
    token_farm.setPriceFeedContract(
        dapp_token.address, price_feed_address, {"from": account}
    )
    # Act
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})

    # Assert
    print(dapp_token.balanceOf(account.address))
    assert (
        token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked
    )
    assert token_farm.uniqueTokensStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address

    return token_farm, dapp_token


def test_issue_tokens(ACTIVE_NETWORK, account, amount_staked):
    # Arrange
    # deploy.ACTIVE_NETWORK = ACTIVE_NETWORK
    if ACTIVE_NETWORK not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    token_farm, dapp_token = test_stake_tokens(ACTIVE_NETWORK, account, amount_staked)

    starting_balance = dapp_token.balanceOf(account.address)

    # Act
    print(token_farm.getUserTotalValue(account))
    print(starting_balance + INITIAL_PRICE_FEED_VALUE)
    token_farm.issueToken({"from": account})

    # Arrange
    # we are staking 1 dapp_token == in price 1 ETH
    # so we should get 2000 dapp tokens in reward
    # since the price of eth is 2,000
    assert (
        dapp_token.balanceOf(account.address)
        == starting_balance + INITIAL_PRICE_FEED_VALUE
    )


def test_get_user_total_value_with_different_tokens(
    ACTIVE_NETWORK, account, amount_staked, random_erc20
):
    # Arrange
    token_farm, dapp_token = test_stake_tokens(ACTIVE_NETWORK, account, amount_staked)
    token_farm.addAllowedTokens(random_erc20.address, {"from": account})
    token_farm.setPriceFeedContract(
        random_erc20.address, get_contract("eth_usd_price_feed"), {"from": account}
    )
    random_erc20_stake_amount = amount_staked * 2
    random_erc20.approve(
        token_farm.address, random_erc20_stake_amount, {"from": account}
    )
    token_farm.stakeTokens(
        random_erc20_stake_amount, random_erc20.address, {"from": account}
    )
    # Assert
    total_value = token_farm.getUserTotalValue(account.address)
    assert total_value == INITIAL_PRICE_FEED_VALUE * 3


def test_get_token_value(ACTIVE_NETWORK):
    # Arrange
    if ACTIVE_NETWORK not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    token_farm, dapp_token = deploy_token_farm_dapp_token()
    # Act / Assert
    assert token_farm.getTokenValue(dapp_token.address) == (
        INITIAL_PRICE_FEED_VALUE,
        DECIMALS,
    )


def test_get_token_value(ACTIVE_NETWORK):
    # Arrange
    if ACTIVE_NETWORK not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    token_farm, dapp_token = deploy_token_farm_dapp_token()
    # Act / Assert
    assert token_farm.getTokenValue(dapp_token.address) == (
        INITIAL_PRICE_FEED_VALUE,
        DECIMALS,
    )


def test_unstake_tokens(ACTIVE_NETWORK, amount_staked):
    # Arrange
    if ACTIVE_NETWORK not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    token_farm, dapp_token = test_stake_tokens(ACTIVE_NETWORK, account, amount_staked)
    # Act
    token_farm.unstakeTokens(dapp_token.address, {"from": account})
    assert dapp_token.balanceOf(account.address) == KEPT_BALANCE
    assert token_farm.stakingBalance(dapp_token.address, account.address) == 0
    assert token_farm.uniqueTokensStaked(account.address) == 0


def test_add_allowed_tokens(ACTIVE_NETWORK):
    # Arrange
    if ACTIVE_NETWORK not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    deploy.ACTIVE_NETWORK = ACTIVE_NETWORK
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_dapp_token()
    # Act
    token_farm.addAllowedTokens(dapp_token.address, {"from": account})
    # Assert
    assert token_farm.allowedTokens(0) == dapp_token.address
    # with pytest.raises(exceptions.VirtualMachineError):
    #     token_farm.addAllowedTokens(dapp_token.address, {"from": non_owner})
