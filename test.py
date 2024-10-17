def find_max_arbitrage(asks, bids, chain):
    if not asks or not bids or (len(asks) == 1 and asks[0][1] == 0) or (len(bids) == 1 and bids[0][1] == 0):
        return []

    # Преобразуем строки в числа
    asks = [(float(price), float(amount)) for price, amount in asks]
    bids = [(float(price), float(amount)) for price, amount in bids]

    # Сортируем asks по цене (по возрастанию) и bids по цене (по убыванию)
    asks.sort(key=lambda x: x[0])  # Для покупки
    bids.sort(key=lambda x: x[0], reverse=True)  # Для продажи

    max_profit = -round(float(chain[2]) * asks[0][0], 2)  # Инициализируем с отрицательной стоимостью из chain

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

    # Если max_profit меньше или равно 0, возвращаем пустой результат
    print(max_profit)
    print(round(float(chain[2]) * asks[0][0], 2) )
    if max_profit <= 0:
        return []

    # Рассчитываем процентную прибыль
    profit_percentage = (max_profit / total_buy_cost) * 100 if total_buy_cost > 0 else 0
    return {
        "max_profit": max_profit,
        "total_buy_cost": total_buy_cost,
        "profit_percentage": profit_percentage,
        "best_trades": best_trades
    }
