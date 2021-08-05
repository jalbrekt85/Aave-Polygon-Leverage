from brownie import config, network, accounts, interface
from scripts.utils import *


class Controller:
    def __init__(self, token_data: dict[str, str]):
        assert all(addr in token_data for addr in ('address', 'amAddress', 'debtAddress'))
        self.account = accounts[0] if network.show_active() == 'polygon-main-fork' else accounts.add(config['wallet']['key'])
        lending_pool = interface.ILendingPoolAddressesProvider('0xd05e3E715d945B59290df0ae8eF85c1BdB684744')
        lending_addr = lending_pool.getLendingPool()
        self.lending_pool = interface.ILendingPool(lending_addr)
        self.router = interface.IUniswapRouterV2("0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff")
        self.matic = '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270'
        self.token = token_data['address']
        self.amToken = token_data['amAddress']
        self.debtToken = token_data['debtAddress']
    
    def balanceOf(self, erc20):
        return ERC20(erc20).balanceOf(self.account.address)

    def approve_all(self):
        erc20 = ERC20(self.token)
        for contract in [self.lending_pool.address, self.router.address]:
            tx_hash = erc20.approve(contract, 1000000 * 10**18, {"from": self.account})
            tx_hash.wait(1)

    def get_erc20(self, amount_wei):
        tx = self.router.swapExactETHForTokens(0, [self.matic, self.token], self.account.address, 9999999999999999, {"from": self.account, "value": amount_wei})
        tx.wait(1)

    def deposit_erc20(self, amount_wei):
        tx = self.lending_pool.deposit(self.token, amount_wei, self.account.address, 0, {"from": self.account})
        tx.wait(1)
    
    def borrow_erc20(self, amount_wei):
        tx = self.lending_pool.borrow(
            self.token,
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

    def repay_erc20(self, amount_wei):
        tx = self.lending_pool.repay(
            self.token,
            amount_wei,
            2,
            self.account.address,
            {'from': self.account},
    )
        tx.wait(1)


    def withdraw_erc20(self, amount_wei):
        tx = self.lending_pool.withdraw(
            self.token,
            amount_wei,
            self.account.address,
            {'from': self.account},
    )
        tx.wait(1)