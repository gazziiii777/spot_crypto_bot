def find_max_arbitrage(asks, bids):
    # Преобразуем строки в числа
    asks = [(float(price), float(amount)) for price, amount in asks]
    bids = [(float(price), float(amount)) for price, amount in bids]

    # Сортируем asks по цене (по возрастанию) и bids по цене (по убыванию)
    asks.sort(key=lambda x: x[0])  # Для покупки
    bids.sort(key=lambda x: x[0], reverse=True)  # Для продажи

    max_profit = 0
    total_buy_cost = 0
    best_trades = []

    ask_index, bid_index = 0, 0

    while ask_index < len(asks) and bid_index < len(bids):
        ask_price, ask_amount = asks[ask_index]
        bid_price, bid_amount = bids[bid_index]

        # Если цена продажи выше цены покупки, ищем прибыль
        if bid_price > ask_price:
            trade_amount = min(ask_amount, bid_amount)
            profit = (bid_price - ask_price) * trade_amount
            trade_buy_cost = ask_price * trade_amount  # Сумма покупки в долларах

            if profit > 0:
                max_profit += profit
                total_buy_cost += trade_buy_cost
                best_trades.append({
                    "buy_price": ask_price,
                    "sell_price": bid_price,
                    "trade_amount": trade_amount,
                    "profit": profit,
                    "total_buy_cost": trade_buy_cost
                })

            # Уменьшаем объемы сделок
            ask_amount -= trade_amount
            bid_amount -= trade_amount

            # Если в ask ордере не осталось объема, переходим к следующему ask
            if ask_amount == 0:
                ask_index += 1
            else:
                asks[ask_index] = (ask_price, ask_amount)

            # Если в bid ордере не осталось объема, переходим к следующему bid
            if bid_amount == 0:
                bid_index += 1
            else:
                bids[bid_index] = (bid_price, bid_amount)

        else:
            # Если цена продажи ниже цены покупки, переходим к следующему ask
            ask_index += 1

    # Рассчитываем процентную прибыль
    profit_percentage = (max_profit / total_buy_cost) * 100 if total_buy_cost > 0 else 0

    return {
        "max_profit": max_profit,
        "total_buy_cost": total_buy_cost,
        "profit_percentage": profit_percentage,
        "best_trades": best_trades
    }


# Пример данных
asks = [['0.010285', '1121.25'], ['0.010387', '1925.39'], ['0.010422', '6716.52'], ['0.010439', '1915.82'],
        ['0.010486', '979.40'], ['0.010492', '1906.28'], ['0.010511', '6659.91'], ['0.010544', '1896.80'],
        ['0.01056', '4922.09'], ['0.010597', '1887.36']]
bids = [['0.013', '1944.7'], ['0.0129', '6831.19'], ['0.010276', '1954.42'], ['0.010183', '1215.42'],
        ['0.010182', '1964.19'], ['0.010161', '6889.25'], ['0.010135', '9109.93'], ['0.010133', '8578.82'],
        ['0.010132', '1974.01'], ['0.010081', '1983.88']]

# Найдем максимальную выгоду
result = find_max_arbitrage(asks, bids)

# Вывод результатов
print(f"Максимальная прибыль: ${result['max_profit']:.2f}")
print(f"Суммарно потрачено на покупку: ${result['total_buy_cost']:.2f}")
print(f"Процент прибыли: {result['profit_percentage']:.2f}%")

# Детализация каждой сделки
for trade in result['best_trades']:
    print(f"Куплено по цене: {trade['buy_price']:.6f}, Продано по цене: {trade['sell_price']:.6f}, "
          f"Объем: {trade['trade_amount']:.2f}, Прибыль: ${trade['profit']:.2f}, "
          f"Потрачено на покупку: ${trade['total_buy_cost']:.2f}")
