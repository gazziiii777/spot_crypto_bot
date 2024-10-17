import bitget.bitget_api_fun.v2.spot.order_api as maxOrderApi
import bitget.bitget_api_fun.bitget_api as baseApi
import bitget.bitget_api_fun.v2.spot.wallet_api as walletApi
import aiohttp
import asyncio
from databases.db_coin_functions import get_chain_with_min_time
from bitget.bitget_api_fun.exceptions import BitgetAPIException

apiKey = ""
secretKey = ''''''
passphrase = ""

baseApi = baseApi.BitgetApi(apiKey, secretKey, passphrase)


# ---------------------------------------------------------------------------------------
# Функции для чекера которые находят валидные монеты для bitget

# Получение всех монет на бирже
def all_coins():
    try:
        response = baseApi.get("/api/v2/spot/public/coins", {})
        with open('../coins/coins_bitget_incorrect', 'w', encoding='utf-8') as file:
            for i in response["data"]:
                file.write(i['coin'] + '\n')
    except BitgetAPIException as e:
        print("error:" + e.message)


# Выделяем тольок монеты которые можно купить/продать на споте
def all_coins_correct():
    try:
        with open('../coins/coins_bitget_incorrect', 'r', encoding='utf-8') as file:
            with open('../coins/coins_bitget', 'w', encoding='utf-8') as new_file_handle:
                for line in file:
                    params = {}
                    params["symbol"] = line.strip() + "USDT"
                    params["limit"] = "5"
                    try:
                        response = baseApi.get("/api/v2/spot/market/orderbook", params)
                        new_file_handle.write(line.strip() + '\n')
                    except BitgetAPIException as e:
                        print("error:" + e.message)
    except BitgetAPIException as e:
        print("error:" + e.message)


# ---------------------------------------------------------------------------------------


# # Отправляем 20 запросов для получения цены покупки и цены продажи в стакане
# async def fetch_orderbook(session, symbol):
#     url = "https://api.bitget.com/api/v2/spot/market/orderbook"
#     params = {
#         "symbol": symbol + "USDT",
#         "limit": "5"
#     }
#     try:
#         async with session.get(url, params=params) as response:
#             result = await response.json()
#             print(result)
#     except Exception as e:
#         print(f"Error fetching {symbol}: {str(e)}")
#
#
# async def process_coins():
#     # Получаем массив из функции get_coins_with_bitget_1
#     coins = get_coins_with_bitget()
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for i, symbol in enumerate(coins):
#             task = asyncio.ensure_future(fetch_orderbook(session, symbol))
#             tasks.append(task)
#
#             # Ограничиваем количество одновременных запросов
#             if len(tasks) >= 20:  # Отправляем по 20 запросов одновременно
#                 await asyncio.gather(*tasks)
#                 tasks = []
#                 await asyncio.sleep(1)  # Пауза в 1 секунду после выполнения 20 запросов
#         # Обрабатываем оставшиеся запросы
#         if tasks:
#             await asyncio.gather(*tasks)


# ---------------------------------------------------------------------------------------
# Пример отправки монет с bitget
# walletApi = walletApi.WalletApi(apiKey, secretKey, passphrase)
#
#
# def wal():
#     try:
#         params = {}
#         params["coin"] = "USDT"
#         params["transferType"] = "on_chain"
#         params["address"] = "0xacbf175ab7d2c3bc41d861e434d42d6b61d2c9c2"
#         params["chain"] = "bep20"
#         params["size"] = "0.4"
#         response = walletApi.withdrawal(params)
#         print(response)
#     except BitgetAPIException as e:
#         print("error:" + e.message)


# Получаем баланс USDT на бирже bitget
def get_balance_usdt_bitget():
    try:
        response = baseApi.get("/api/v2/spot/account/assets", {})
        for balance in response['data']:
            if balance['coin'] == 'USDT':
                return balance['available']
    except BitgetAPIException as e:
        print("error:" + e.message)


# Функция для coin_checker получает кошельки ее пока закоментировал тк не юзаю
# def get_all_deposit_address_bitget():
#     try:
#         response_1 = baseApi.get("/api/v2/spot/public/coins", {})
#         for i in response_1['data']:
#             for j in i['chains']:
#                 try:
#                     params = {}
#                     params['coin'] = i['coin']
#                     params['chain'] = j['chain']
#                     response = baseApi.get("/api/v2/spot/wallet/deposit-address", params)
#                     add_address_if_not_exists('bitget', response['data']['address'], response['data']['chain'],
#                                               response['data']['tag'])
#                 except:
#                     print(i['coin'])
#     except BitgetAPIException as e:
#         print("error:" + e.message)

# Получение цены в стакане (она была просто для теста сейчас она не нужна
# def get_orderbook():
#     try:
#         params = {}
#         params['symbol'] = "AINUSDT"
#         params['limit'] = 10
#         response = baseApi.get("/api/v2/spot/market/orderbook", params)
#         print(response)
#     except BitgetAPIException as e:
#         print("error:" + e.message)

# Функция которая нахдит все сети для вывода (для опредленной ментки), а через get_chain_time находит из этих сетей самую быструю
def get_coin_chain_bitget_withdrawal(coin):
    try:
        bitget_chains_withdrawal = []
        params = {'coin': coin}
        response = baseApi.get("/api/v2/spot/public/coins", params)
        for chain_withdrawal_info in response['data'][0]['chains']:
            if chain_withdrawal_info['withdrawable'] == "true" and chain_withdrawal_info['congestion'] == 'normal':
                bitget_chains_withdrawal.append(
                    [chain_withdrawal_info['chain'], chain_withdrawal_info['needTag'],
                     chain_withdrawal_info['withdrawFee']])

        return bitget_chains_withdrawal
    except BitgetAPIException as e:
        print("error:" + e.message)


get_coin_chain_bitget_withdrawal('USDT')


# Функция которая возвращяает цену по которой можно купить монетку на споте
def get_asks_bitget(coin):
    try:
        params = {}
        params['symbol'] = coin + "USDT"
        params['limit'] = 10
        response = baseApi.get("/api/v2/spot/market/orderbook", params)
        print(response['data']['asks'])
        return response['data']['asks']
    except:
        return []

# if __name__ == '__main__':
# Выставление ордера на покупку
# maxOrderApi = maxOrderApi.OrderApi(apiKey, secretKey, passphrase)
# try:
#     params = {}
#     params["symbol"] = "DOGSUSDT"
#     params["side"] = "sell"
#     params["orderType"] = "limit"
#     params["force"] = "gtc"
#     params["price"] = "10000"
#     params["size"] = "10"
#     response = maxOrderApi.placeOrder(params)
#     print(response)
# except BitgetAPIException as e:
#     print("error:" + e.message)

# Demo 2:place order by post directly
# try:
#     params = {}
#     params["symbol"] = "BTCUSDT_UMCBL"
#     params["marginCoin"] = "USDT"
#     params["side"] = "open_long"
#     params["orderType"] = "limit"
#     params["price"] = "27012"
#     params["size"] = "0.01"
#     params["timInForceValue"] = "normal"
#     response = baseApi.post("/api/mix/v1/order/placeOrder", params)
#     print(response)
# except BitgetAPIException as e:
#     print("error:" + e.message)

# Получение всех монет на бирже
# try:
#     response = baseApi.get("/api/v2/spot/public/coins", {})
#     with open('../coins/coins_bitget_incorrect', 'w', encoding='utf-8') as file:
#         for i in response["data"]:
#             file.write(i['coin'] +'\n')
# except BitgetAPIException as e:
#     print("error:" + e.message)

# Получение информации о монете
# try:
#     params = {}
#     params["coin"] = "USDT"
#     response = baseApi.get("/api/v2/spot/public/coins", params)
#     print(response)
# except BitgetAPIException as e:
#     print("error:" + e.message)

# Получение адресса для депозита
# try:
#     response = baseApi.get("/api/v2/spot/wallet/deposit-address?coin=USDT&chain=trc20", {})
# except BitgetAPIException as e:
#     print("error:" + e.message)

# Отправка монет

# Проверка монетки на волидность
# try:
#     with open('../coins/coins_bitget_incorrect', 'r', encoding='utf-8') as file:
#         with open('../coins/coins_bitget', 'w', encoding='utf-8') as new_file_handle:
#             for line in file:
#                 params = {}
#                 params["symbol"] = line.strip() + "USDT"
#                 params["limit"] = "10"
#                 try:
#                     response = baseApi.get("/api/v2/spot/market/orderbook", params)
#                     new_file_handle.write(line.strip() + '\n')
#                 except BitgetAPIException as e:
#                     print("error:" + e.message)
# except BitgetAPIException as e:
#     print("error:" + e.message)
