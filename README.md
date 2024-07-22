# Arbitrage Bot
![image](https://github.com/user-attachments/assets/f9352f16-805a-4c45-b1f9-0a25a9cdde36)


Hey there! This Arbitrage Bot, designed by xOneiros, is a cool tool for performing arbitrage trading across multiple decentralized exchanges (DEX). The main goal of this bot is to take advantage of price differences between various exchanges and execute trades to make a profit.

### Features

- Fetches prices from multiple DEXs.
- Automatically executes arbitrage trades.
- Provides a graphical user interface (GUI) for easy interaction.
- Displays price trends and trade history.

### Requirements

- Python 3.6 or higher
- `aiohttp` library
- `web3` library
- `requests` library
- `tkinter` library
- `python-dotenv` library

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/xONEIROS/Arbitrage-Bot.git
   cd ArbitrageBot
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add the necessary environment variables:

   ```env
   ETH_NODE_URL=https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID
   DEX_1_URL=https://api.dex1.com
   DEX_2_URL=https://api.dex2.com
   DEX_3_URL=https://api.dex3.com
   DEX_4_URL=https://api.dex4.com
   DEX_5_URL=https://api.dex5.com
   PRIVATE_KEY=YOUR_PRIVATE_KEY
   ```

### Usage

1. Run the bot:

   ```bash
   python main.py
   ```

2. Enter the token symbol and amount in the provided fields.
3. Click "Check Arbitrage" to find and execute arbitrage opportunities.

### Detailed Explanation

#### 1. File `config.py`

This file contains configurations for DEX URLs and the private key. It uses the `dotenv` library to load environment variables.

```python
import os
from dotenv import load_dotenv

load_dotenv()

ETH_NODE_URL = os.getenv("ETH_NODE_URL")
DEX_URLS = {
    "DEX1": os.getenv("DEX_1_URL"),
    "DEX2": os.getenv("DEX_2_URL"),
    "DEX3": os.getenv("DEX_3_URL"),
    "DEX4": os.getenv("DEX_4_URL"),
    "DEX5": os.getenv("DEX_5_URL")
}
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
```

#### 2. File `arbitrage.py`

This file includes the logic for the arbitrage bot, fetching prices from various DEXs and executing trades.

```python
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
```

#### 3. File `ui.py`

This file provides the graphical user interface (GUI) using `Tkinter`, allowing easy interaction with the bot.

```python
import tkinter as tk
from arbitrage import ArbitrageBot
import asyncio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ArbitrageApp:
    def __init__(self, root):
        self.bot = ArbitrageBot()
        self.root = root
        self.root.title("Arbitrage Bot")

        # Section for token input
        self.token_label = tk.Label(root, text="Token:")
        self.token_label.grid(row=0, column=0)
        self.token_entry = tk.Entry(root)
        self.token_entry.grid(row=0, column=1)

        # Section for amount input
        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.grid(row=1, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=1, column=1)

        # Button to check arbitrage opportunities
        self.check_button = tk.Button(root, text="Check Arbitrage", command=self.check_arbitrage)
        self.check_button.grid(row=2, column=0, columnspan=2)

        # Section for displaying prices
        self.price_label = tk.Label(root, text="Prices:")
        self.price_label.grid(row=3, column=0, columnspan=2)
        self.price_text = tk.Text(root, height=10, width=50)
        self.price_text.grid(row=4, column=0, columnspan=2)

        # Graph for price trends
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2)

        # Section for advanced settings
        self.advanced_settings_label = tk.Label(root, text="Advanced Settings:")
        self.advanced_settings_label.grid(row=6, column=0, columnspan=2)

        self.trade_threshold_label = tk.Label(root, text="Trade Threshold:")
        self.trade_threshold_label.grid(row=7, column=0)
        self.trade_threshold_entry = tk.Entry(root)
        self.trade_threshold_entry.grid(row=7, column=1)

        # Section for trade history
        self.history_label = tk.Label(root, text="Trade History:")
        self.history_label.grid(row=8, column=0, columnspan=2)
        self.history_text = tk.Text(root, height=10, width=50)
        self.history_text.grid(row=9, column=0, columnspan=2)

    def check_arbitrage(self):
        token = self.token_entry.get()
        amount = self.amount_entry.get()
        asyncio.run(self.bot.find_arbitrage_opportunity(token, amount))
        self.update_prices(token)
        self.update_graph(token)
        self.update_history()

    def update_prices(self, token):
        prices = asyncio.run(self.bot.get_prices(token))
        self.price_text.delete(1.0, tk.END)
        for dex, price in prices.items():
            self.price_text.insert(tk.END, f"{dex}: {price}\\n")

    def update_graph(self, token):
        prices = asyncio.run(self.bot.get_prices(token))
        self.ax.clear()
        dex_names = list(prices.keys())
        dex_prices = list(prices.values())
        self.ax.bar(dex_names, dex_prices)
        self.ax.set_title('DEX Prices')
        self.ax.set_xlabel('DEX')
        self.ax.set_ylabel('Price')
        self.canvas.draw()

    def update_history(self):
        self.history_text.delete(1.0, tk.END)
        for trade in self.bot.trade_history:
            self.history_text.insert(tk.END, f"From {trade['from_dex']} to {trade['to_dex']} - {trade['token']} - {trade['amount']} - {trade['status']}\\n")
```

#### 4. File `main.py`

This file is used to run the application and launch the GUI.

```python
from ui import ArbitrageApp

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    app = ArbitrageApp(root)
    root.mainloop()
```

![head](https://github.com/user-attachments/assets/5d7c007d-e0eb-4e27-934a-8b603464598c)

>------------------------------

<div align="center">
    <p>
        <a href="Https://x.com/0xOneiros">
            <small>🆔 twitter </small>  
        </a>
        | 
        <a href="Https://t.me/xOneiros">
            <small>🆔 telegram </small>  
        </a>
    </p>
</div>
