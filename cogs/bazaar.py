import discord
from discord.ext import commands, tasks
import json
from loguru import logger
import aiohttp
from utils.format import *
from utils.getdata import *

with open('data/database.json') as d:
    database = json.load(d)


class Bazaar(commands.Cog):

    def __init__(self, client):
        self.client = client



    @commands.Cog.listener()
    async def on_ready(self):
        self.cachebazaar.start()
        print('Bazaar is ready.')


    
    
    @tasks.loop(minutes=1)
    async def cachebazaar(self):
        try:
            data = await getbzdata()
            if data["success"] is False:
                cause = data["cause"]
                logger.error(f"Error caching bazaar: {cause}")
            else:
                data = data["products"]
                new_data = {}
                for product in data:
                    sell_price = data[product]["quick_status"]["sellPrice"]
                    sell_volume = data[product]["quick_status"]["sellVolume"]
                    sell_orders = data[product]["quick_status"]["sellOrders"]
                    buy_price = data[product]["quick_status"]["buyPrice"]
                    buy_volume = data[product]["quick_status"]["buyVolume"]
                    buy_orders = data[product]["quick_status"]["buyOrders"]
                    if product == "CARROT_ITEM":
                        product = "CARROT"
                    if product == "POTATO_ITEM":
                        product = "POTATO"
                    if product == "ENCHANTED_HUGE_MUSHROOM_2":
                        product = "ENCHANTED_RED_MUSHROOM_BLOCK"
                    if product == "ENCHANTED_HUGE_MUSHROOM_1":
                        product = "ENCHANTED_BROWN_MUSHROOM_BLOCK"
                    if product == "HUGE_MUSHROOM_1":
                        product = "BROWN_MUSHROOM_BLOCK"
                    if product == "HUGE_MUSHROOM_2":
                        product = "RED_MUSHROOM_BLOCK"
                    if product == "LOG_2:1":
                        product = "DARK_OAK_LOG"
                    if product == "LOG:1":
                        product = "SPRUCE_LOG"
                    if product == "LOG:3":
                        product = "JUNGLE_LOG"
                    if product == "LOG:2":
                        product = "BIRCH_LOG"
                    if product == "LOG":
                        product = "OAK_LOG"
                    if product == "LOG_2":
                        product = "ACACIA_LOG"
                    if product == "ENCHANTED_LAPIS_LAZULI_BLOCK":
                        product = "ENCHANTED_LAPIS_BLOCK"
                    if product == "ENCHANTED_LAPIS_LAZULI":
                        product = "ENCHANTED_LAPIS"
                    if product == "ENCHANTED_LAPIS_LAZULI_BLOCK":
                        product = "ENCHANTED_LAPIS_BLOCK"
                    if product == "SNOW_BALL":
                        product = "SNOW"
                    if product == "ENCHANTED_NETHER_STALK":
                        product = "ENCHANTED_NETHER_WART"
                    if product == "NETHER_STALK":
                        product = "NETHER_WART"
                    if product == "RAW_FISH:3":
                        product = "PUFFERFISH"
                    if product == "RAW_FISH:2":
                        product = "CLOWNFISH"
                    if product == "RAW_FISH:1":
                        product = "RAW_SALMON"
                    if product == "ENCHANTED_WATER_LILY":
                        product = "ENCHANTED_LILY_PAD"
                    if product == "WATER_LILY":
                        product = "LILYPAD"
                    if product == "SUPER_EGG":
                        product = "SUPER_ENCHANTED_EGG"
                    if product == "SULPHUR":
                        product = "GUNPOWDER"
                    if product == "CLAY_BALL":
                        product = "CLAY"
                    if product == "ENCHANTED_CLAY_BALL":
                        product = "ENCHANTED_CLAY"



                    new_data[product] = {
                        "sell_price": sell_price,
                        "sell_volume": sell_volume,
                        "sell_orders": sell_orders,
                        "buy_price": buy_price,
                        "buy_volume": buy_volume,
                        "buy_orders": buy_orders
                    }
                with open('bazaar/bazaardata.json', 'w') as f:
                    json.dump(new_data, f, indent=4)
                logger.info("Bazaar data cached.")

        except Exception as e:
            logger.error(f"Error caching bazaar: {e}")




def setup(client):
    client.add_cog(Bazaar(client))