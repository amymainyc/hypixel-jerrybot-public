import os
from discord.ext import commands
from loguru import logger
import logging
import json

with open("data/database.json") as f:
    data = json.load(f)

token = data["token"]
client = commands.Bot(command_prefix=['j.', 'J.'], case_insensitive=True)
client.remove_command('help')


def load_cogs():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            client.load_extension(f"cogs.{name}")
            logger.info(f"Loaded cogs.{name}")



load_cogs()

client.run(token)
