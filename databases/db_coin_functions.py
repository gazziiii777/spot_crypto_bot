import sqlite3
import os
import pandas as pd


# Функция универсальная, она записывает монетки ей нужно подавать монетку и биржу
def add_coin_db(coin_value, exchange):
    # Открываем соединение внутри функции
    with sqlite3.connect(r'D:\pythonProject\spot_arbitrage_bot\databases\coins.db') as conn:
        cursor = conn.cursor()
        # Проверяем, существует ли уже такой coin в базе данных
        cursor.execute("SELECT * FROM coins WHERE coin = ?", (coin_value,))
        record = cursor.fetchone()

        if record is None:
            # Если такой coin не существует, добавляем новую запись с bitget = 1
            cursor.execute(f"INSERT INTO coins (coin, {exchange}) VALUES (?, ?)", (coin_value, 1))
        else:
            # Если coin уже существует, обновляем значение bitget на 1
            cursor.execute(f"UPDATE coins SET {exchange} = 1 WHERE coin = ?", (coin_value,))

        # Сохраняем изменения в базе данных
        conn.commit()


# ---------------------------------------------------------------------------------------
# Функция для coin_checker
def add_coins_bitget():
    # Открываем файл и обрабатываем каждую строку
    with open('../coins/coins_bitget', 'r') as file:
        for line in file:
            coin_value = line.strip()  # Удаляем лишние пробелы и символы новой строки
            if coin_value:  # Если строка не пустая
                add_coin_db(coin_value, "bitget")
    # Удаляем файлы после завершения работы
    os.remove('../coins/coins_bitget')
    os.remove('../coins/coins_bitget_incorrect')


# def get_coins_with_bitget():
#     # Открываем соединение внутри функции
#     with sqlite3.connect(r'D:\pythonProject\spot_arbitrage_bot\databases\coins.db') as conn:
#         cursor = conn.cursor()
#         # Массив для хранения значений coin, где bitget = 1
#         coins_with_bitget_1 = []
#
#         # Запрос к базе данных для получения всех строк, где bitget = 1
#         cursor.execute("SELECT coin FROM coins WHERE bitget = 1")
#
#         # Проход по результатам запроса и добавление значений coin в массив
#         rows = cursor.fetchall()
#         for row in rows:
#             coins_with_bitget_1.append(row[0])  # Добавляем значение coin в массив
#
#     # Возвращаем массив значений coin
#     return coins_with_bitget_1

# Функция для добюавляения кошелько, но пока что она использоваться не будет
# def add_address_if_not_exists(exchange, address, chain, tag):
#     # Подключаемся к базе данных внутри функции
#     with sqlite3.connect(r'D:\pythonProject\spot_arbitrage_bot\databases\address.db') as conn:
#         cursor = conn.cursor()
#
#         # Проверяем, есть ли уже такой адрес в таблице
#         cursor.execute(f'SELECT * FROM address WHERE {exchange}_address = ?', (address,))
#         result = cursor.fetchone()
#
#         # Если такого адреса нет, добавляем его
#         if result is None:
#             cursor.execute(
#                 f'INSERT INTO address ({exchange}_address, {exchange}_chain, {exchange}_chain_tag) VALUES (?, ?, ?)',
#                 (address, chain, tag))
#             print(f'Address {address} added with chain {chain}.')
#         else:
#             print(f'Address {address} already exists.')
#
#         # Фиксируем изменения
#         conn.commit()


# Важная функция которую нужно переписать и сделать унверсальной, она пока что работает только для bitget (Логика должна быфть такая: Мы перендаем в эту функцию биржу и она возвращает 2 другие где тоже стоят 1, нужно сделать так чтобы она была легко модифиуцирована для болльшего кол-во бирж
def filter_coins_bitget():
    # Открываем соединение внутри функции
    with sqlite3.connect(r'D:\pythonProject\spot_arbitrage_bot\databases\coins.db') as conn:
        # Чтение данных из таблицы
        query = "SELECT * FROM coins"
        df = pd.read_sql(query, conn)

    # Инициализируем два массива
    matching_mexc = []
    matching_bingx = []

    # Пройдем по каждой строке
    for index, row in df.iterrows():
        if row['bitget'] == 1:
            # Если mexc == 1, добавляем в массив mexc
            if row['mexc'] == 1:
                matching_mexc.append(row['coin'])
            # Если bingx == 1, добавляем в массив bingx
            if row['bingx'] == 1:
                matching_bingx.append(row['coin'])

    return matching_mexc, matching_bingx


# Этой функции подается массив сетей и она находит самую быструю (для всех бирж можно использовать) пример входных данных [['BTC', 'false', '0.0001'], ['BEP20', 'false', '0.00000638']]
def get_chain_with_min_time(chains_withdrawal, chains_deposit):
    chains_present = [chain for chain in chains_withdrawal if chain[0] in chains_deposit]
    chain_with_min_time = []
    with sqlite3.connect(r'D:\pythonProject\spot_arbitrage_bot\databases\chains.db') as conn:
        cursor = conn.cursor()

        for chain in chains_present:
            # Проверяем, есть ли уже такой адрес в таблице по chainName
            cursor.execute(f'SELECT * FROM chains WHERE chainName = ?', (chain[0],))
            result_chainName = cursor.fetchone()

            # Проверяем, есть ли уже такой адрес в таблице по chainNameBig
            cursor.execute(f'SELECT * FROM chains WHERE chainNameBig = ?', (chain[0],))
            result_chainNameBig = cursor.fetchone()

            # Если найден результат в любой из таблиц
            if result_chainName is not None:
                result_time = int(result_chainName[2])
            elif result_chainNameBig is not None:
                result_time = int(result_chainNameBig[2])
            else:
                continue  # Если ничего не найдено, пропускаем итерацию

            # Проверка для минимального времени
            if chain_with_min_time:
                if int(chain_with_min_time[-1]) > result_time:
                    chain_with_min_time = chain
                    chain_with_min_time.append(result_time)
            else:
                chain_with_min_time = chain
                chain_with_min_time.append(result_time)
    print('minTime:', chain_with_min_time)
    return chain_with_min_time
    # Пример вызова функции для биржи bitget
# exchange_name = 'bitget'
# mexc_coins, bingx_coins = filter_coins(exchange_name)
#
# print("Coins matching mexc:", mexc_coins)
# print("Coins matching bingx:", bingx_coins)
