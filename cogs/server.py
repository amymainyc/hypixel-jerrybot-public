from discord.ext import commands
import discord
import json
from discord.ext import tasks
from datetime import datetime
import asyncio
from loguru import logger


with open('data/database.json') as d:
    database = json.load(d)


class Server(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener()
    async def on_message(self, ctx):

        # auction messages
        if ctx.channel == self.client.get_channel(712820393324445722):
            if ctx.author == self.client.get_user(729064195345350668):
                embed = ctx.embeds[0]
                channel = self.client.get_channel(762888691043270687)
                await asyncio.sleep(2)
                await channel.send(embed=embed)

        else:
            return



def setup(client):
    client.add_cog(Server(client))
