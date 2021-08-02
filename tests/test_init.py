from scripts.controller import Controller
import pytest
from brownie import Contract
from brownie.network.account import Account

@pytest.fixture(scope="module")
def controller():
    return Controller()

def test_account_init(controller):
    assert isinstance(controller.account, Account)

def test_lending_pool_init(controller):
    assert isinstance(controller.lending_pool, Contract)

