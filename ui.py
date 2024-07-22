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
            self.price_text.insert(tk.END, f"{dex}: {price}\n")

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
            self.history_text.insert(tk.END, f"From {trade['from_dex']} to {trade['to_dex']} - {trade['token']} - {trade['amount']} - {trade['status']}\n")
