from scripts.controller import Controller
import pytest
from brownie import Contract
from brownie.network.account import Account
from scripts.marketdata import market_data
from scripts.utils import *

dai_addr = market_data['dai']['address']
amDai_addr = market_data['dai']['amAddress']
debtDai_addr = market_data['dai']['debtAddress']

@pytest.fixture(scope="module")
def controller():
    return Controller(market_data['dai'])


def test_eth_to_erc_swap(controller):

    assert controller.account.balance() > 0
    assert controller.balanceOf(dai_addr) == 0
    
    controller.approve_all()
    controller.get_erc20(controller.account.balance() / 2)

    assert controller.balanceOf(dai_addr) > 0

def test_aave_deposit_erc(controller):

    controller.deposit_erc20(controller.balanceOf(dai_addr))
    
    assert controller.balanceOf(amDai_addr) > 0

def test_aave_borrow_erc(controller):


    assert controller.balanceOf(debtDai_addr) == 0
    
    controller.borrow_erc20(controller.get_stable_borrow_amount())

    assert controller.balanceOf(debtDai_addr) > 0

    controller.deposit_erc20(controller.balanceOf(dai_addr))
    

def test_aave_withdraw_erc(controller):

    assert controller.balanceOf(amDai_addr) > 0

    before_balance = controller.balanceOf(dai_addr)

    withdraw_amount = int((controller.balanceOf(amDai_addr) - controller.balanceOf(debtDai_addr)) * 0.4)
    controller.withdraw_erc20(withdraw_amount)

    assert controller.balanceOf(dai_addr) > before_balance

def test_aave_repay_erc(controller):
    balance = controller.balanceOf(dai_addr)
    debt = controller.balanceOf(debtDai_addr)

    assert balance > 0
    assert debt > 0

    controller.repay_erc20(balance)

    assert controller.balanceOf(debtDai_addr) < debt