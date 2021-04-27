from discord.ext import commands
import discord
import json
from loguru import logger
from discord.ext import tasks
import base64
import aiohttp
import asyncio


with open('data/database.json') as d:
    database = json.load(d)


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Jerry is ready.')
        link = database["shortlink"]
        activity = discord.Game(name=f"j.help | {link}")
        # activity = discord.Game(name="Bot testing in progress.")
        await self.client.change_presence(status=discord.Status.online, activity=activity)
        await asyncio.sleep(43200)
        self.push.start()


    @commands.command()
    async def hi(self, ctx):
        if ctx.author != self.client.get_user(430079880353546242):
            return
        await ctx.send('Jerry.')


    @commands.command()
    async def invite(self, ctx):
        await ctx.send('Invite Jerry to your server using this link:\n' + database["shortlink"])


    @commands.command()
    async def vote(self, ctx):
        await ctx.send('Vote for Jerry using this link:\n' + database["votelink"])


    @commands.command()
    async def support(self, ctx):
        await ctx.send('Join the community/support server here:\n' + database["supportlink"])


    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="Jerry's Commands",
            color=0xf00000
        )
        embed.set_footer(
            text='More features in development!'
        )
        embed.set_thumbnail(url="https://i.imgur.com/6lOTQhe.png")
        embed.add_field(
            name="j.help",
            value="Responds with this message",
            inline=False
        )
        embed.add_field(
            name="j.invite",
            value="Responds with the invite link for Jerry!",
            inline=False
        )
        embed.add_field(
            name="j.vote",
            value="Responds with the vote link for Jerry!",
            inline=False
        )
        embed.add_field(
            name="j.support",
            value="Responds with the invite to the support server.",
            inline=False
        )
        embed.add_field(
            name="j.skills (username) (profile)",
            value="Shows the user's Skyblock skill levels.",
            inline=False
        )
        embed.add_field(
            name="j.accessories (username) (profile)",
            value="Shows the user's missing accessories.",
            inline=False
        )
        embed.add_field(
            name="j.armor (username) (profile)",
            value="Shows the user's equipped armor.",
            inline=False
        )
        embed.add_field(
            name="j.inventory (username) (profile)",
            value="Shows the user's inventory."
                  "\n Aliases: `j.inv`",
            inline=False
        )
        embed.add_field(
            name="j.dungeons (username) (profile)",
            value="Shows the user's dungeon stats"
                  "\n Aliases: `j.dungeon`",
            inline=False
        )
        embed.add_field(
            name="j.auctions (username)",
            value="Shows the user's active auctions"
                  "\n Aliases: `j.ah`",
            inline=False
        )
        embed.add_field(
            name="j.lowestbin (item name)",
            value="Returns the lowest BIN price for the given item."
                  "\n Aliases: `j.bin`",
            inline=False
        )
        embed.add_field(
            name="j.bazaar (item name)",
            value="Returns the bazaar prices for the given item."
                  "\n Aliases: `j.bz`",
            inline=False
        )
        embed.add_field(
            name="j.setupreminders/j.disabledreminders",
            value="Allows you to set up Skyblock event reminders for the channel.",
            inline=False
        )
        await ctx.send(embed=embed)


    @tasks.loop(minutes=120)
    async def push(self):
        logger.info('Pushing files to Github...')
        await self.pushdata()


    async def pushdata(self):
        filenames = ["data/eventchannels.json"]
        for filename in filenames:
            try:
                token = database["github_oath"]
                repo = "amymainyc/jerrybot"
                branch = "master"
                url = "https://api.github.com/repos/" + repo + "/contents/" + filename

                base64content = base64.b64encode(open(filename, "rb").read())

                async with aiohttp.ClientSession() as session:
                    async with session.get(url + '?ref=' + branch, headers={"Authorization": "token " + token}) as data:
                        data = await data.json()
                sha = data['sha']

                if base64content.decode('utf-8') + "\n" != data['content']:
                    message = json.dumps(
                        {"message": "Automatic data update.",
                         "branch": branch,
                         "content": base64content.decode("utf-8"),
                         "sha": sha}
                    )

                    async with aiohttp.ClientSession() as session:
                        async with session.put(url, data=message,
                                               headers={"Content-Type": "application/json",
                                                        "Authorization": "token " + token}) as resp:
                            print(resp)
                else:
                    print("Nothing to update.")
            except Exception as e:
                logger.exception(e)


    @commands.command()
    async def gitPush(self, ctx):
        if ctx.author != self.client.get_user(430079880353546242):
            return
        filenames = ["data/eventchannels.json"]
        for filename in filenames:
            try:
                token = database["github_oath"]
                repo = "amymainyc/jerrybot"
                branch = "master"
                url = "https://api.github.com/repos/" + repo + "/contents/" + filename

                base64content = base64.b64encode(open(filename, "rb").read())

                async with aiohttp.ClientSession() as session:
                    async with session.get(url + '?ref=' + branch, headers={"Authorization": "token " + token}) as data:
                        data = await data.json()
                sha = data['sha']

                if base64content.decode('utf-8') + "\n" != data['content']:
                    message = json.dumps(
                        {"message": "Automatic data update.",
                         "branch": branch,
                         "content": base64content.decode("utf-8"),
                         "sha": sha}
                    )

                    async with aiohttp.ClientSession() as session:
                        async with session.put(url, data=message,
                                               headers={"Content-Type": "application/json",
                                                        "Authorization": "token " + token}) as resp:
                            print(resp)
                else:
                    print("Nothing to update.")
            except Exception as e:
                logger.exception(e)
        await ctx.send("Pushed latest data to GitHub.")



def setup(client):
    client.add_cog(Admin(client))
