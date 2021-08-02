from brownie import interface


def ERC20(token_address):
    return interface.IERC20(token_address)

def eth_rate():
    oracle = interface.EACAggregatorProxy("0xF9680D99D6C9589e2a93a78A04A279e509205945")
    return oracle.latestAnswer() / 100000000
