import dbl
from discord.ext import commands, tasks
import json
from loguru import logger

with open('data/database.json') as d:
    database = json.load(d)

class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = database["dbltoken"] 
        self.dblpy = dbl.DBLClient(self.bot, self.token)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.check_guilds.start()

    @tasks.loop(minutes=30)
    async def check_guilds(self):
        await self.dblpy.post_guild_count()
        logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))

def setup(bot):
    bot.add_cog(TopGG(bot))