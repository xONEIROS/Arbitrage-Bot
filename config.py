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
