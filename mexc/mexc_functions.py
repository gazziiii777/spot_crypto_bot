from pymexc import spot
from databases.db_coin_functions import add_coin_db
import re

api_key = ""
api_secret = ""

# Инициализация клиента
spot_client = spot.HTTP(api_key=api_key, api_secret=api_secret)


# def get_withdraw_wallets(asset):
#     # Получение адреса для вывода для конкретного актива
#     wallet = spot_client.deposit_address(asset)
#
#     # Печать результата
#     print(f"Address: {wallet}")

# Функция для coin_checker, все монетки для mexc и закидывает их в db
def get_all_coins():
    exchange_info = spot_client.exchange_info()
    for coin in exchange_info['symbols']:
        if coin['isSpotTradingAllowed'] and coin['symbol'].endswith("USDT"):
            add_coin_db(coin['symbol'].replace("USDT", ""), "mexc")


# Функция которая получает баланс на mexc в USDT
def get_balance_usdt_mexc():
    account_info = spot_client.account_information()
    # Перебор всех активов и вывод баланса
    for asset in account_info['balances']:
        if asset['asset'] == 'USDT':
            return asset['free']


# def get_chain_address(coin, network):
#     return [spot_client.generate_deposit_address(coin=coin, network=network)['address'],
#             spot_client.generate_deposit_address(coin=coin, network=network)['memo']]


# Функция для получения всех кошельков, но мы ее наврное использовать не будем
# def get_deposit_address_mexc():
#     for address_info in spot_client.get_currency_info():
#         for info in address_info['networkList']:
#             try:
#                 address_full_info = get_chain_address(info['coin'], info['network'])
#                 match = re.search(r'\((.*?)\)', info['network'])
#                 add_address_if_not_exists('mexc', address_full_info[0], match.group(1), address_full_info[1])
#             except:
#                 print('error')
#                 print(info['coin'], info['network'])

# Функция для мекса mexc, она проверяет можно ли высталяеть ордер на споте для этой монетки
def get_isSpotTradingAllowed_mexc(coin):
    info = spot_client.exchange_info(coin + 'USDT')
    if info['symbols'][0]['isSpotTradingAllowed']:
        return True
    else:
        return False


# Функция которая возращвет значинеия по которой мождно продать эту монетку (зеленый стакан)
def get_bids_mexc(coin):
    return spot_client.order_book(coin + "USDT", 10)['bids']


# Функцию которю нужно дописать, она проверяет доступна ли монетка для депозита
def get_deposit_enable_mexc(coin):
    chains_deposit = []
    for all_chains_deposit in spot_client.get_currency_info():
        if all_chains_deposit['coin'] == coin:
            for chain_deposit in all_chains_deposit['networkList']:
                if chain_deposit['depositEnable'] and re.findall(r'\((.*?)\)', chain_deposit['network']) != []:
                    chains_deposit += re.findall(r'\((.*?)\)', chain_deposit['network'])
                    chains_deposit += re.findall(r'([^\(]+)\(', chain_deposit['network'])
    return chains_deposit


get_deposit_enable_mexc('USDT')
# addresses = spot_client.deposit_address(coin=

# spot_client.generate_deposit_address(coin='USDT', network='TRX20')
# print(addresses)

# get_deposit_address_mexc()
# get_deposit_address_mexc()
# Вызов функции для вывода адресов для конкретного актива, например, BTC
# get_withdraw_wallets("USDT")
