import os
from discord.ext import commands
from loguru import logger
import logging


token = 'NzI5MDY0MTk1MzQ1MzUwNjY4.XwDhpQ.SxWIR8697LGI7fk4HX1c76HqN8Q'
client = commands.Bot(command_prefix='j.', case_insensitive=True)
client.remove_command('help')


def load_cogs():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            client.load_extension(f"cogs.{name}")
            logger.info(f"Loaded cogs.{name}")



load_cogs()

client.run(token)
