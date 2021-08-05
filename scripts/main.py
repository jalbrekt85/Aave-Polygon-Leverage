
from scripts.controller import Controller
from scripts.marketdata import market_data
from web3 import Web3
# network.connect()

dai_addrs =  {'address': "0x8f3cf7ad23cd3cadbd9735aff958023239c6a063", "amAddress": "0x27f8d03b3a2196956ed754badc28d73be8830a6e", "debtAddress": "0x75c4d1Fb84429023170086f06E682DcbBF537b7d"}
dai = dai_addrs['address']
amDai = dai_addrs['amAddress']
debtDai = dai_addrs['debtAddress']


def stack_tokens(user: Controller):
    for _ in range(6):
        user.deposit_erc20(user.balanceOf(dai))
        user.borrow_erc20(user.get_stable_borrow_amount())
    user.deposit_erc20(user.balanceOf(dai))

def cash_out(user: Controller):
    while user.balanceOf(debtDai) > 0:
        withdraw_amount = int((user.balanceOf(amDai) - user.balanceOf(debtDai)) * 0.4)
        user.withdraw_erc20(withdraw_amount)
        user.repay_erc20(user.balanceOf(dai))

def main():
    user = Controller(dai_addrs)
    user.approve_all()
    user.get_erc20(user.account.balance() * 0.9)
    
    stack_tokens(user)


if __name__ == '__main__':
    main()