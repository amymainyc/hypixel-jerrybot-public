import aiohttp
import json
import discord
from loguru import logger

with open('data/database.json') as d:
    database = json.load(d)

async def checkplayer(ctx, param):
    if ctx.author.bot:
        return
    errormessage = "Please include the required fields: "\
                    "\nj.(command) (username) (profile <optional>)"
    if len(param) != 2 and len(param) != 1:
        await ctx.send(errormessage)
        return

    username = param[0]
    mcdata = await checkusername(username)
    if mcdata == -1:
        await ctx.send('Please enter a valid username.')
        return
    playeruuid = mcdata[1]
    playername = mcdata[0]

    if len(param) == 1:
        profile = ''
    else:
        profile = param[1]
    profile = profile.lower().capitalize()

    try:
        playerstats = await getstatdata(playername, playeruuid, profile)
    except Exception as e:
        await ctx.send('Error reaching the API. Please try again in a few minutes.')
        logger.exception(e)
        return

    if "error" in playerstats:
        await ctx.send(f"Error getting player data: Haven't played Skyblock and/or wrong profile name.")
        return
    return [playerstats, playername, playeruuid]

async def checkusername(arg):
    try: 
        async with aiohttp.ClientSession() as session:
            async with session.get(database["api_mcuser"].replace("[user]", arg)) as data:
                data = await data.json()
        return [data["name"], data["id"]]
    except:
        return -1

async def checkuuid(arg):
    async with aiohttp.ClientSession() as session:
        async with session.get(database["api_mcuuid"].replace("[uuid]", arg)) as data:
            data = await data.json()
    return data[0]["name"]

async def getstatdata(name, uuid, profile):
    link = database["api_stats"].replace('[uuid]', uuid).replace('[profile]', profile)
    logger.info(f"Getting stats for {name}: {link}")
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as data:
            return await data.json()

def getauctiondata():
        with open('auction/auctiondata.json') as d:
            data = json.load(d)
            return data

async def checkdungeonplayer(ctx, param):
    if ctx.author.bot:
        return
    errormessage = "Please include the following parameters: " \
                    "\n`username`, `profile``"
    if len(param) != 2 and len(param) != 1:
        await ctx.send(errormessage)
        return

    username = param[0]
    if checkusername(username) == -1:
        await ctx.send('Invalid Username!')
        return

    playername = checkusername(username)[1]
    playeruuid = checkusername(username)[0]

    if len(param) == 1:
        profile = ''
    else:
        profile = param[1]
        profile = profile.lower().capitalize()

    try:
        playerstats = await getdungeondata(playername, playeruuid)
    except Exception as e:
        await ctx.send('Error reaching the API. Please try again in a few minutes.')
        logger.exception(e)
        return

    if playerstats["success"] is False:
        await ctx.send(f"Error getting player data: Please try again later.")
        print(playerstats)
        return

    if playerstats["profiles"] is None:
        await ctx.send(f"Error getting player data: Haven't played Skyblock.")
        return

    if profile != '':
        playerprofiles = []
        for activeprofile in playerstats["profiles"]:
            playerprofiles.append(activeprofile["cute_name"])
            if profile == activeprofile["cute_name"]:
                playerstats = activeprofile
        if profile not in playerprofiles:
            await ctx.send(f"Error getting player data: Invalid profile name.")
            return
    else:
        try:
            mostrecent = 0
            for activeprofile in playerstats["profiles"]:
                try:
                    lastsave = activeprofile["members"][playeruuid]["last_save"]
                    if lastsave > mostrecent:
                        mostrecent = lastsave
                        playerstats = activeprofile
                        profile = playerstats["cute_name"]
                except:
                    pass
        except Exception as e:
            logger.exception(e)
            await ctx.send(f"Error getting profile data: Try specifying a profile.")
            return
    return [profile, playerstats, playername, playeruuid]

async def getdungeondata(name, uuid): 
    link = database["api_dungeons"].replace('[key]', database["apikey2"])
    link = link.replace('[uuid]', uuid)
    print(f"Getting dungeon stats for {name}: {link}")
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as data:
            return await data.json()

async def getbzdata():
        async with aiohttp.ClientSession() as session:
            async with session.get(database["api_bazaar"].replace('[key]', database["apikey2"])) as data:
                return await data.json()