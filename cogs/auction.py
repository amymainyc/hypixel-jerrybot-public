import discord
import aiohttp
from discord.ext import commands, tasks
import json
from loguru import logger
import asyncio
from utils.getdata import *
from utils.format import *

with open('data/database.json') as d:
    database = json.load(d)


class Auction(commands.Cog):

    def __init__(self, client):
        self.client = client




    @commands.Cog.listener()
    async def on_ready(self):
        self.main.start()
        await asyncio.sleep(120)
        self.updatebins.start()
        print('Auction is Ready.')




    @tasks.loop(seconds=60)
    async def main(self):
        try:
            await self.cacheandcheck()
            logger.info("Auction cache started")
        except Exception as e:
            logger.exception(e)




    async def cacheandcheck(self):
        sample = await self.getahdata(0)
        if sample["success"] is True:
            numpages = sample["totalPages"]
            auctions = {}
            bins = {}
            for page in range(numpages):
                data = await self.getahdata(page)
                if data["success"] is True:
                    # print(page)
                    data = data["auctions"]
                    for auction in data:
                        # sort bin auctions
                        if "bin" in auction:
                            if auction["item_name"] == "Enchanted Book":
                                itemname = auction["item_lore"]
                            else:
                                itemname = auction["item_name"]
                            if itemname not in bins:
                                bins[itemname] = []
                                bins[itemname].append(self.addbin(auction))
                            else:
                                bins[itemname].append(self.addbin(auction))
                            # check bin auction
                            await self.checkitem(self.addbin(auction), itemname, auction["uuid"])
                        # sort regular auctions
                        auctioneer = auction["auctioneer"]
                        if auctioneer not in auctions:
                            auctions[auctioneer] = []
                            auctions[auctioneer].append(self.addauction(auction))
                        else:
                            auctions[auctioneer].append(self.addauction(auction))
                    await asyncio.sleep(.1)
                else:
                    logger.warning('Auction data unavailable; Cause: ' + data["cause"])

            if auctions != {}:
                with open('auction/auctiondata.json', 'w') as f:
                    json.dump(auctions, f, indent=4)
            if bins != {}:
                with open('auction/bindata.json', 'w') as f:
                    json.dump(bins, f, indent=4)
            logger.info('Auction data cached.')
        else:
            logger.info('Sample data unavailable; Cause: ' + sample["cause"])

    def addbin(self, auction):
        userauction = {
            "tier": auction["tier"].lower(),
            "starting_bid": auction["starting_bid"],
            "auctioneer": auction["auctioneer"],
        }

        return userauction

    def addauction(self, auction):
        userauction = {"item_name": auction["item_name"], "end": auction["end"], "tier": auction["tier"],
                       "starting_bid": auction["starting_bid"], "highest_bid": auction["highest_bid_amount"]}
        if "bin" in auction:
            userauction["bin"] = True
        else:
            userauction["bin"] = False
        return userauction




    async def checkitem(self, auction, itemname, uuid):
        # check if uuid has been checked before
        f = open("auction/pastbins.txt")
        pastauctions = f.read().split('\n')
        f.close()

        if uuid in pastauctions:
            pass
        else:
            itemprice = auction["starting_bid"]
            itemtier = auction["tier"]
            with open('auction/binlist.json', 'r') as b:
                aimbins = json.load(b)

            # check if item names match
            for aimname in aimbins:
                if aimname in itemname.lower():
                    # check if item tiers match
                    for aimtier in aimbins[aimname]:
                        if aimtier == "any" or aimtier in itemtier:
                            # check if prices are right
                            if itemprice <= aimbins[aimname][aimtier] * .75:
                                auctioneer = await checkuuid(auction["auctioneer"])
                                logger.info('Auction found by user: ' + auctioneer)
                                embed = self.makeembed(
                                    auctioneer,
                                    itemname,
                                    itemprice,
                                    itemtier,
                                    aimbins[aimname][aimtier]
                                )
                                f = open("auction/pastbins.txt", "w")
                                f.write('\n'.join(pastauctions[1:]) + '\n' + uuid)
                                f.close()
                                channel = self.client.get_channel(712820393324445722)
                                await channel.send(embed=embed)

    async def getahdata(self, page):
        async with aiohttp.ClientSession() as session:
            async with session.get(database["api_auctions"].replace('[page]', str(page)).replace('[key]', database["apikey1"])) as data:
                return await data.json()

    def makeembed(self, player, itemname, price, tier, lowestbin):
        profit = lowestbin - price
        profit = price_formatter(profit)
        lowestbin = price_formatter(lowestbin)
        price = price_formatter(price)
        tier = tier[0].upper() + tier[1:]
        embed = discord.Embed(
            title='Underpriced Auction!'
        )
        embed.add_field(
            name=f"`/ah {player}`", 
            value=f"{itemname}\nTier: {tier}\nPrice: {price} coins \n\nNext Lowest: {lowestbin} coins\nPotential Profit: {profit} coins"
        )
        return embed



    @tasks.loop(minutes=5)
    async def updatebins(self):
        logger.info("Updating lowest BIN prices.")
        with open('auction/binlist.json', 'r') as b:
            aimbins = json.load(b)
        with open('auction/bindata.json', 'r') as b:
            bins = json.load(b)

        # check if item names and rarities match
        for aimitem in aimbins:
            for aimrarity in aimbins[aimitem]:
                lowestbin = 0

                # if looking for specific rarity
                if aimrarity != "any":
                    for item in bins:
                        # check item name
                        if aimitem.lower() in item.lower():
                            for auction in bins[item]:
                                # check rarity
                                if auction["tier"] == aimrarity:
                                    # check if it's the lowest price
                                    if lowestbin == 0 or auction["starting_bid"] < lowestbin:
                                        lowestbin = auction["starting_bid"]
                    if lowestbin != 0:
                        aimbins[aimitem][aimrarity] = lowestbin

                # if not looking for specific rarity
                else:
                    for item in bins:
                        # check item name
                        if aimitem.lower() in item.lower():
                            for auction in bins[item]:
                                # check if it's the lowest price
                                if lowestbin == 0 or auction["starting_bid"] < lowestbin:
                                    lowestbin = auction["starting_bid"]
                    if lowestbin != 0:
                        aimbins[aimitem][aimrarity] = lowestbin

        with open('auction/binlist.json', 'w') as f:
            json.dump(aimbins, f, indent=4)
        logger.info('Lowest BIN prices updated.')

    @commands.command()
    async def updatebinlist(self, ctx):
        if ctx.author != self.client.get_user(430079880353546242):
            return
        logger.info("Updating lowest BIN prices.")
        with open('auction/binlist.json', 'r') as b:
            aimbins = json.load(b)
        with open('auction/bindata.json', 'r') as b:
            bins = json.load(b)

        # check if item names and rarities match
        for aimitem in aimbins:
            for aimrarity in aimbins[aimitem]:
                lowestbin = 0

                # if looking for specific rarity
                if aimrarity != "any":
                    for item in bins:
                        # check item name
                        if aimitem.lower() in item.lower():
                            for auction in bins[item]:
                                # check rarity
                                if auction["tier"] == aimrarity:
                                    # check if it's the lowest price
                                    if lowestbin == 0 or auction["starting_bid"] < lowestbin:
                                        lowestbin = auction["starting_bid"]
                    if lowestbin != 0:
                        aimbins[aimitem][aimrarity] = lowestbin

                # if not looking for specific rarity
                else:
                    for item in bins:
                        # check item name
                        if aimitem.lower() in item.lower():
                            for auction in bins[item]:
                                # check if it's the lowest price
                                if lowestbin == 0 or auction["starting_bid"] < lowestbin:
                                    lowestbin = auction["starting_bid"]
                    if lowestbin != 0:
                        aimbins[aimitem][aimrarity] = lowestbin

        with open('auction/binlist.json', 'w') as f:
            json.dump(aimbins, f, indent=4)
        logger.info('Lowest BIN prices updated.')
        await ctx.send('Updated latest BINs.')




def setup(client):
    client.add_cog(Auction(client))
