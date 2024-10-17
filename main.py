import asyncio
from bitget.bitget_functions import get_balance_usdt_bitget, get_coin_chain_bitget_withdrawal, get_asks_bitget
from bingx.bingx_functions import get_balance_usdt_bingx
from mexc.mexc_functions import get_balance_usdt_mexc, get_isSpotTradingAllowed_mexc, get_bids_mexc, \
    get_deposit_enable_mexc
from databases.db_coin_functions import filter_coins_bitget, get_chain_with_min_time
from test import find_max_arbitrage


# Надо дописать проверку для мекса что depositEnable
async def bitget_pars():
    while True:
        if float(get_balance_usdt_bitget()) < 100:
            bitget_mexc, bitget_bingx = filter_coins_bitget()
            for coin in bitget_mexc:
                chain_with_min_time = get_chain_with_min_time(get_coin_chain_bitget_withdrawal(coin),
                                                              get_deposit_enable_mexc(coin))
                print(coin)
                print(chain_with_min_time)
                if chain_with_min_time and get_isSpotTradingAllowed_mexc(coin):
                    result = find_max_arbitrage(get_asks_bitget(coin), get_bids_mexc(coin), chain_with_min_time)
                    if result:
                        print(f"Максимальная прибыль: ${result['max_profit']:.2f}")
                        print(f"Суммарно потрачено на покупку: ${result['total_buy_cost']:.2f}")
                        print(f"Процент прибыли: {result['profit_percentage']:.2f}%")
                        print(coin)
                        # Детализация каждой сделки
                        for trade in result['best_trades']:
                            print(f"Куплено по цене: {trade['buy_price']:.6f}, Продано по цене: {trade['sell_price']:.6f}, "
                                  f"Объем: {trade['trade_amount']:.2f}, Прибыль: ${trade['profit']:.2f}, "
                                  f"Потрачено на покупку: ${trade['total_buy_cost']:.2f}")
                    # print(get_bids_mexc(coin))
                    # print(get_asks_bitget(coin))
                    # print(chain_withdrawal_info)
        else:
            await asyncio.sleep(5)
        pass


async def bingx_pars():
    while True:
        if float(get_balance_usdt_bingx()) > 100:
            print(1)
        else:
            await asyncio.sleep(5)
        pass


async def mexc_pars():
    while True:
        if float(get_balance_usdt_mexc()) > 100:
            print(1)
        else:
            await asyncio.sleep(5)
        pass


async def main():
    await asyncio.gather(
        bitget_pars(),
        bingx_pars(),
        mexc_pars()
    )


if __name__ == "__main__":
    asyncio.run(main())
