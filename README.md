# Arbitrage Bot

## Description
This bot performs arbitrage trading across multiple decentralized exchanges (DEX). It checks the prices of tokens on different DEXs and executes trades to take advantage of price differences.

## Features
- Fetches prices from multiple DEXs.
- Executes arbitrage trades automatically.
- Provides a graphical user interface for easy interaction.
- Displays price trends and trade history.

## Requirements
- Python 3.6+
- `aiohttp` library
- `web3` library
- `requests` library
- `tkinter` library
- `dotenv` library

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
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

## Usage
1. Run the bot:
   ```bash
   python main.py
   ```

2. Enter the token symbol and amount in the provided fields.
3. Click "Check Arbitrage" to find and execute arbitrage opportunities.

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