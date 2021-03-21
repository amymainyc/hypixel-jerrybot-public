import os
from discord.ext import commands
from loguru import logger
import json

with open('data/database.json') as d:
    database = json.load(d)


token = database["token"]
client = commands.Bot(command_prefix='j.')
client.remove_command('help')


def load_cogs():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            try:
                client.load_extension(f"cogs.{name}")
                logger.info(f"Loaded cogs.{name}")
            except Exception as e:
                logger.error(f"Jerry couldn't load: {name}.")
                logger.exception(e)

load_cogs()

client.run(token)
