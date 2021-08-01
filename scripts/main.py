
from brownie import network, accounts, config

# network.connect()
print(network.show_active())

def main():
    print(config['wallets']['key'])

if __name__ == '__main__':
    main()