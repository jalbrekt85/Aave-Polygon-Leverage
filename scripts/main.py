
from brownie import network, accounts, config
from scripts.controller import Controller
# network.connect()

def main():
    print(Controller().address)
    print()

if __name__ == '__main__':
    main()