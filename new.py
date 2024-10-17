import aiohttp
import asyncio


# Отправляем 20 запросов для получения цены покупки и цены продажи в стакане
async def fetch_orderbook(session, symbol):
    url = "https://api.bitget.com/api/v2/spot/market/orderbook"
    params = {
        "symbol": symbol + "USDT",
        "limit": "10"
    }
    try:
        async with session.get(url, params=params) as response:
            result = await response.json()
            print(result)
    except Exception as e:
        print(f"Error fetching {symbol}: {str(e)}")


async def process_file():
    async with aiohttp.ClientSession() as session:
        tasks = []
        with open('coins/coins_bitget', 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                symbol = line.strip()
                task = asyncio.ensure_future(fetch_orderbook(session, symbol))
                tasks.append(task)

                # Ограничиваем количество одновременных запросов
                if len(tasks) >= 20:  # Отправляем по 20 запросов одновременно
                    await asyncio.gather(*tasks)
                    tasks = []
                    await asyncio.sleep(1)  # Пауза в 1 секунду после выполнения 20 запросов

        # Обрабатываем оставшиеся запросы
        if tasks:
            await asyncio.gather(*tasks)


# Запуск асинхронного процесса
asyncio.run(process_file())
