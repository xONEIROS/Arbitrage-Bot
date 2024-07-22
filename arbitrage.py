import asyncio
from web3 import Web3
import aiohttp
from config import ETH_NODE_URL, DEX_URLS, PRIVATE_KEY
import logging

class ArbitrageBot:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))
        self.account = self.web3.eth.account.privateKeyToAccount(PRIVATE_KEY)
        self.trade_history = []
        logging.basicConfig(level=logging.INFO)

    async def get_price(self, session, dex_url, token):
        try:
            async with session.get(f"{dex_url}/price?token={token}") as response:
                response.raise_for_status()
                data = await response.json()
                return data["price"]
        except aiohttp.ClientError as e:
            logging.error(f"Error fetching price from {dex_url}: {e}")
            return None

    async def get_prices(self, token):
        prices = {}
        async with aiohttp.ClientSession() as session:
            tasks = [self.get_price(session, dex_url, token) for dex_url in DEX_URLS.values()]
            results = await asyncio.gather(*tasks)
            for dex_name, price in zip(DEX_URLS.keys(), results):
                if price:
                    prices[dex_name] = price
        return prices

    async def execute_trade(self, from_dex, to_dex, token, amount):
        try:
            # Logic for executing trade between DEXs
            trade_details = {
                'from_dex': from_dex,
                'to_dex': to_dex,
                'token': token,
                'amount': amount,
                'status': 'success'
            }
            self.trade_history.append(trade_details)
            logging.info(f"Executed trade from {from_dex} to {to_dex} for {amount} {token}")
        except Exception as e:
            trade_details = {
                'from_dex': from_dex,
                'to_dex': to_dex,
                'token': token,
                'amount': amount,
                'status': 'failed',
                'error': str(e)
            }
            self.trade_history.append(trade_details)
            logging.error(f"Error executing trade: {e}")

    async def find_arbitrage_opportunity(self, token, amount):
        prices = await self.get_prices(token)
        if not prices:
            return

        sorted_prices = sorted(prices.items(), key=lambda x: x[1])
        if len(sorted_prices) > 1:
            await self.execute_trade(sorted_prices[0][0], sorted_prices[-1][0], token, amount)
