from scripts.controller import Controller
import pytest
from brownie import Contract
from brownie.network.account import Account
from scripts.marketdata import market_data
from scripts.utils import *
from brownie.network.rpc import Rpc
@pytest.fixture(scope="module")
def controller():
    return Controller()

def test_approve():
    pass


def test_eth_to_erc_swap(controller):
    dai_addr = market_data['dai']['address']

    assert controller.account.balance() > 0
    assert ERC20(dai_addr).balanceOf(controller.account.address) == 0
    
    controller.approve_all(dai_addr)
    controller.get_erc20(dai_addr, controller.account.balance() / 2)

    assert ERC20(dai_addr).balanceOf(controller.account.address) > 0

def test_aave_deposit_erc(controller):
    dai_addr = market_data['dai']['address']
    amDai_addr = market_data['dai']['amAddress']

    controller.deposit_erc20(dai_addr, ERC20(dai_addr).balanceOf(controller.account.address))
    
    assert ERC20(amDai_addr).balanceOf(controller.account.address) > 0

def test_aave_borrow_erc(controller):
    dai_addr = market_data['dai']['address']
    amDai_addr = market_data['dai']['amAddress']
    debtDai_addr = market_data['dai']['debtAddress']

    assert ERC20(debtDai_addr).balanceOf(controller.account.address) == 0
    
    controller.borrow_erc20(dai_addr, controller.get_stable_borrow_amount())

    assert ERC20(debtDai_addr).balanceOf(controller.account.address) > 0
