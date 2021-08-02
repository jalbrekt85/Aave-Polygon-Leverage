from brownie import config, network, accounts, interface
from scripts.marketdata import market_data
from scripts.utils import *


class Controller:
    def __init__(self) -> None:
        self.account = accounts[0] if network.show_active() == 'polygon-main-fork' else accounts.add(config['wallet']['key'])
        lending_pool = interface.ILendingPoolAddressesProvider('0xd05e3E715d945B59290df0ae8eF85c1BdB684744')
        lending_addr = lending_pool.getLendingPool()
        self.lending_pool = interface.ILendingPool(lending_addr)
        self.router = interface.IUniswapRouterV2("0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff")
        self.matic = market_data['matic']['address']

    def approve_all(self, token_address):
        erc20 = ERC20(token_address)
        for contract in [self.lending_pool.address, self.router.address]:
            tx_hash = erc20.approve(contract, 1000000 * 10**18, {"from": self.account})
            tx_hash.wait(1)

    def get_erc20(self, token_address, amount_wei):
        tx = self.router.swapExactETHForTokens(0, [self.matic, token_address], self.account.address, 9999999999999999, {"from": self.account, "value": amount_wei})
        tx.wait(1)

    def deposit_erc20(self, token_address, amount_wei):
        tx = self.lending_pool.deposit(token_address, amount_wei, self.account.address, 0, {"from": self.account})
        tx.wait(1)
    
    def borrow_erc20(self, token_address, amount_wei):
        tx = self.lending_pool.borrow(
            token_address,
            amount_wei,
            2,
            0,
            self.account.address,
            {'from': self.account},
    )
        tx.wait(1)
    
    def get_stable_borrow_amount(self):
        (_,_,available_borrow_eth,_,_,_,) = self.lending_pool.getUserAccountData(self.account.address)
        available_borrow_stable = (available_borrow_eth * eth_rate()) * 0.95
        return available_borrow_stable

    def repay_erc20(self, token_address, amount):
        tx = self.lending_pool.repay(
            token_address,
            amount,
            2,
            self.account.address,
            {'from': self.account},
    )
        tx.wait(1)

    def withdraw_erc20(self, token_address, amount):
        tx = self.lending_pool.withdraw(
            token_address,
            amount,
            self.account.address,
            {'from': self.account},
    )
        tx.wait(1)