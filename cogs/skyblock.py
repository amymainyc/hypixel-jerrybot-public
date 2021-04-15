import discord
from discord.ext import commands
import datetime
from datetime import datetime
import json
from loguru import logger
import aiohttp
from utils.format import *
from utils.getdata import *

with open('data/database.json') as d:
    database = json.load(d)


class Skyblock(commands.Cog):

    def __init__(self, client):
        self.client = client




    @commands.Cog.listener()
    async def on_ready(self):
        print('Jerry is ready.')




    @commands.command()
    async def skills(self, ctx, *param):
        data = await checkplayer(ctx, param)
        if data is None: 
            return
        playerstats = data[0]
        playeruuid = data[2]
        playername = data[1]
        if len(param) == 1:
            profile = ''
        else:
            profile = param[1]
        profile = profile.lower().capitalize()

        # all checks passed
        try:
            skills = playerstats["members"][playeruuid]["skills"]

            # calculate average
            skillcount = 0
            skilllevelcount = 0
            for skill in skills:
                if skill == 'carpentry' or skill == 'runecrafting':
                    pass
                else:
                    skillcount += 1
                    skilllevelcount += skills[skill]["level"]
            if skillcount < 8:
                error = f"Skills are not available for {playername} due to limited API access. "
                error2 = f"\n[See here](https://sky.lea.moe/resources/video/enable_api.webm) " \
                         f"how to enable full API access"
                embed = discord.Embed(title="Limited API Access", color=0xf00000)
                embed.add_field(name=error, value=error2)
                await ctx.send(embed=embed)
                return
            else:
                averageskilllvl = str(round(skilllevelcount / skillcount, 2))

            skill_data = {}
            for skill in skills:
                skill_data[skill] = {
                    "level": str(skills[skill]["level"]),
                    "total": price_formatter(round(skills[skill]["xp"])),
                    "progress_bar": '',
                    "progress": str(int(skills[skill]["progress"] * 100)) + '%',
                    "xp_needed": '0'
                }
                if skills[skill]["xpForNext"] is None:
                    skill_data[skill]["xp_needed"] = '0'
                else:
                    skill_data[skill]["xp_needed"] = price_formatter(
                        str(round(skills[skill]["xpForNext"] - skills[skill]["xpCurrent"])))

                if skill_data[skill]["xp_needed"] == '0':
                    progressbar = "[====maxed====]"
                else:
                    progressbar = '['
                    equals = round(skills[skill]["progress"] / (1/12))
                    dashes = 12 - equals
                    progressbar = progressbar + equals * '=' + '|' + dashes * '-' + ']'
                skill_data[skill]["progress_bar"] = progressbar

            all_skills = ["combat", "mining", "farming", "alchemy", "enchanting", "taming", "fishing", "foraging", "carpentry", "runecrafting"]
            for s in all_skills:
                if s not in skill_data:
                    skill_data[s] = {
                        "level": "0",
                        "total": "0",
                        "progress_bar": '[|------------]',
                        "progress": "0%",
                        "xp_needed": "50"
                    }

            # make the embed
            if profile == '':
                embed = discord.Embed(
                    title=f"{playername}'s Skill Levels",
                    color=0xf00000,
                    description=f"Data taken from most recently used profile."
                                f"\nAverage Skill Level: {averageskilllvl}"
                )
            else:
                embed = discord.Embed(
                    title=f"{playername}'s Skill Levels",
                    color=0xf00000,
                    description=f"Data taken from profile: {profile}"
                                f"\nAverage Skill Level: {averageskilllvl}"
                )
            try:
                embed.add_field(
                    name=str('⚔️ Combat Level ' + skill_data["combat"]["level"]),
                    value=str('`' + skill_data["combat"]["progress_bar"] + '`' + skill_data["combat"]["progress"] +
                            "\nTotal XP: " + skill_data["combat"]["total"] +
                            '\nNext Level: ' + skill_data["combat"]["xp_needed"] + 'XP'),
                    inline=True
                )
            except:
                pass
            try:
                embed.add_field(
                    name=str('⛏️ Mining Level ' + skill_data["mining"]["level"]),
                    value=str('`' + skill_data["mining"]["progress_bar"] + '`' + skill_data["mining"]["progress"] +
                            "\nTotal XP: " + skill_data["mining"]["total"] +
                            '\nNext Level: ' + skill_data["mining"]["xp_needed"] + 'XP'),
                    inline=True
                )
            except:
                pass
            try:
                embed.add_field(
                    name=str('🌾️️ Farming Level ' + skill_data["farming"]["level"]),
                    value=str('`' + skill_data["farming"]["progress_bar"] + '`' + skill_data["farming"]["progress"] +
                            "\nTotal XP: " + skill_data["farming"]["total"] +
                            '\nNext Level: ' + skill_data["farming"]["xp_needed"] + 'XP'),

                    inline=True
                )
            except:
                pass
            try:
                embed.add_field(
                    name=str('⚗️️ Alchemy Level ' + skill_data["alchemy"]["level"]),
                    value=str('`' + skill_data["alchemy"]["progress_bar"] + '`' + skill_data["alchemy"]["progress"] +
                            "\nTotal XP: " + skill_data["alchemy"]["total"] +
                            '\nNext Level: ' + skill_data["alchemy"]["xp_needed"] + 'XP'),
                    inline=True
                )
            except:
                pass
            try:
                embed.add_field(
                    name=str('📖 Enchanting Level ' + skill_data["enchanting"]["level"]),
                    value=str('`' + skill_data["enchanting"]["progress_bar"] + '`' + skill_data["enchanting"]["progress"] +
                            "\nTotal XP: " + skill_data["enchanting"]["total"] +
                            '\nNext Level: ' + skill_data["enchanting"]["xp_needed"] + 'XP'),
                    inline=True
                )
            except:
                pass
            try:
                embed.add_field(
                    name=str('🐴 Taming Level ' + skill_data["taming"]["level"]),
                    value=str('`' + skill_data["taming"]["progress_bar"] + '`' + skill_data["taming"]["progress"] +
                            "\nTotal XP: " + skill_data["taming"]["total"] +
                            '\nNext Level: ' + skill_data["taming"]["xp_needed"] + 'XP'),
                    inline=True
                )
            except:
                pass
            try:
                embed.add_field(
                    name=str('🎣 Fishing Level ' + skill_data["fishing"]["level"]),
                    value=str('`' + skill_data["fishing"]["progress_bar"] + '`' + skill_data["fishing"]["progress"] +
                            "\nTotal XP: " + skill_data["fishing"]["total"] +
                            '\nNext Level: ' + skill_data["fishing"]["xp_needed"] + 'XP'),
                    inline=True
                )
            except:
                pass
            try:
                embed.add_field(
                    name=str('🌳 Foraging Level ' + skill_data["foraging"]["level"]),
                    value=str('`' + skill_data["foraging"]["progress_bar"] + '`' + skill_data["foraging"]["progress"] +
                            "\nTotal XP: " + skill_data["foraging"]["total"] +
                            '\nNext Level: ' + skill_data["foraging"]["xp_needed"] + 'XP'),
                    inline=True
                )
            except:
                pass
            try:
                embed.add_field(
                    name=str('🛠 Carpentry Level ' + skill_data["carpentry"]["level"]),
                    value=str('`' + skill_data["carpentry"]["progress_bar"] + '`' + skill_data["carpentry"]["progress"] +
                            "\nTotal XP: " + skill_data["carpentry"]["total"] +
                            '\nNext Level: ' + skill_data["carpentry"]["xp_needed"] + 'XP'),
                    inline=True
                )
            except:
                pass
            try:
                embed.add_field(
                    name=str('🔮 Runecrafting Level ' + skill_data["runecrafting"]["level"]),
                    value=str('`' + skill_data["runecrafting"]["progress_bar"] + '`' + skill_data["runecrafting"]["progress"] +
                            "\nTotal XP: " + skill_data["runecrafting"]["total"] +
                            '\nNext Level: ' + skill_data["runecrafting"]["xp_needed"] + 'XP'),
                    inline=True
                )
            except:
                pass
            

            embed.set_thumbnail(url=f"https://crafatar.com/avatars/{playeruuid}?size=40&default=MHF_Steve&overlay.png")
            embed.add_field(
                name="** **",
                value="Also try: `j.accessories`, `j.armor`, `j.inventory`, `j.dungeons`, `j.auctions`",
                inline=False
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send('Error getting player data. If this persists, feel free to dm me: Moonflower#8861')
            logger.exception(e)




    @commands.command()
    async def accessories(self, ctx, *param):
        data = await checkplayer(ctx, param)
        if data is None: 
            return
        playerstats = data[0]
        playeruuid = data[2]
        playername = data[1]
        if len(param) == 1:
            profile = ''
        else:
            profile = param[1]
        profile = profile.lower().capitalize()

        # all checks passed
        try:
            talisman_bag = playerstats["members"][playeruuid]["talisman_bag"]
            inventory = playerstats["members"][playeruuid]["inventory"]

            # if api is off
            if not talisman_bag and not inventory:
                embed = discord.Embed(title="No Accessory Data", color=0xf00000)
                embed.add_field(
                    name=f"Accesssory data is not available for {playername} due to limited API access. ",
                    value=f"\n[Click here](https://sky.lea.moe/resources/video/enable_api.webm) " \
                         f"to see how to enable full API access"
                    )
                await ctx.send(embed=embed)
                return

            # match accessories with database
            with open("data/accessories.txt", "r") as f:
                accessories = f.read().split("\n")
            total_count = len(accessories)
            accessories_count = 0
            missing_accessories = ""

            for a in accessories:
                missing = True
                for item in talisman_bag:
                    if item != {}:
                        if a in item["name"]:
                            if a == "Beastmaster Crest":
                                if item["rarity"] == "legendary":
                                    accessories_count += 1
                                    missing = False
                                    break
                            else:
                                accessories_count += 1
                                missing = False
                                break
                if missing is True:
                    for item in inventory: 
                        if item != {}:
                            if a in item["name"]:
                                if a == "Beastmaster Crest":
                                    if item["rarity"] == "legendary":
                                        accessories_count += 1
                                        missing = False
                                        break
                                else:
                                    accessories_count += 1
                                    missing = False
                                    break
                if missing is True:
                    if a == "Beastmaster Crest":
                        missing_accessories += "Legendary " + a + "\n"
                    else:
                        missing_accessories += a + "\n"

                

            missing_count = total_count - accessories_count

            if profile == '':
                embed = discord.Embed(
                    title=f"{playername}'s Missing Accessories",
                    color=0xf00000,
                    description=f"Data taken from most recently used profile."
                )
            else:
                embed = discord.Embed(
                    title=f"{playername}'s Missing Accessories",
                    color=0xf00000,
                    description=f"Data taken from profile: {profile}"
                )

            embed.add_field(
                name=f"Missing Accessories ({missing_count}/{total_count})",
                value=missing_accessories
            )
            embed.set_thumbnail(url=f"https://crafatar.com/avatars/{playeruuid}?size=40&default=MHF_Steve&overlay.png")
            embed.add_field(
                name="** **",
                value="Also try: `j.skills`, `j.armor`, `j.inventory`, `j.dungeons`, `j.auctions`",
                inline=False
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send('Error getting player data. If this persists, feel free to dm me: Moonflower#8861')
            logger.exception(e)


    
    
    @commands.command(aliases=["inv"])
    async def inventory(self, ctx, *param):
        data = await checkplayer(ctx, param)
        playerstats = data[0]
        playeruuid = data[2]
        playername = data[1]
        if len(param) == 1:
            profile = ''
        else:
            profile = param[1]
        profile = profile.lower().capitalize()

        # all checks passed
        try:
            inventory = playerstats["members"][playeruuid]["inventory"]

            if not inventory:
                error = f"Inventory data is not available for {playername} due to limited API access. "
                error2 = f"\n[See here](https://sky.lea.moe/resources/video/enable_api.webm) " \
                         f"how to enable full API access"
                embed = discord.Embed(title="No Inventory Data", color=0xf00000)
                embed.add_field(name=error, value=error2)
                await ctx.send(embed=embed)
                return

            items = []
            for item in inventory:
                if item != {}:
                    if item["name"] != "§aSkyBlock Menu §7(Right Click)":
                        item_details = []
                        item_name = item_name_formatter(item["name"])
                        count = str(item["count"])
                        item_details.append(item_name)
                        item_details.append(count)
                        items.append(item_details)
            item_list = ""
            for item in items:
                item_name = item[0]
                count = item[1]
                if item_list != "":
                    item_list += f"\n{item_name} x{count}"
                else:
                    item_list += f"{item_name} x{count}"

            if profile == '':
                embed = discord.Embed(
                    title=f"{playername}'s Inventory",
                    color=0xf00000,
                    description=f"Data taken from most recently used profile."
                )
            else:
                embed = discord.Embed(
                    title=f"{playername}'s Inventory",
                    color=0xf00000,
                    description=f"Data taken from profile: {profile}"
                )
            embed.add_field(name="** **", value=item_list)
            embed.set_thumbnail(url=f"https://crafatar.com/avatars/{playeruuid}?size=40&default=MHF_Steve&overlay.png")
            embed.add_field(
                name="** **",
                value="Also try: `j.skills`, `j.accessories`, `j.armor`, `j.dungeons`, `j.auctions`",
                inline=False
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send('Error getting player data. If this persists, feel free to dm me: Moonflower#8861')
            logger.exception(e)




    @commands.command()
    async def armor(self, ctx, *param):
        data = await checkplayer(ctx, param)
        playerstats = data[0]
        playeruuid = data[2]
        playername = data[1]
        if len(param) == 1:
            profile = ''
        else:
            profile = param[1]
        profile = profile.lower().capitalize()

        # all checks passed
        try:
            armor = playerstats["members"][playeruuid]["armor"]

            if not armor:
                error = f"Armor data is not available for {playername} due to limited API access. "
                error2 = f"\n[See here](https://sky.lea.moe/resources/video/enable_api.webm) " \
                         f"how to enable full API access"
                embed = discord.Embed(title="No Inventory Data", color=0xf00000)
                embed.add_field(name=error, value=error2)
                await ctx.send(embed=embed)
                return

            items = []
            for item in armor:
                if item != {}:
                    item_details = []
                    item_name = item_name_formatter(item["name"])
                    rarity = item["rarity"].capitalize()
                    enchants = enchant_formatter(item["attributes"]["enchantments"])
                    item_details.append(item_name)
                    item_details.append(rarity)
                    item_details.append(enchants)

                    items.append(item_details)


            item_list = []
            for item in items:
                item_name = item[0]
                rarity = item[1]
                enchants = item[2]
                item_desc = f"Rarity: {rarity}" \
                            f"\nEnchants: {enchants}"
                item_details = {
                    "item_name": item_name,
                    "item_desc": item_desc
                }
                item_list.append(item_details)


            if profile == '':
                embed = discord.Embed(
                    title=f"{playername}'s Equipped Armor",
                    color=0xf00000,
                    description=f"Data taken from most recently used profile."
                )
            else:
                embed = discord.Embed(
                    title=f"{playername}'s Equipped Armor",
                    color=0xf00000,
                    description=f"Data taken from profile: {profile}"
                )
            for item in range(len(item_list)):
                item = len(item_list) - item - 1
                item_name = item_list[item]["item_name"]
                item_desc = item_list[item]["item_desc"]
                embed.add_field(name=item_name, value=item_desc, inline=False)

            embed.set_thumbnail(url=f"https://crafatar.com/avatars/{playeruuid}?size=40&default=MHF_Steve&overlay.png")
            embed.add_field(
                name="** **",
                value="Also try: `j.skills`, `j.accessories`, `j.inventory`, `j.dungeons`, `j.auctions`",
                inline=False
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send('Error getting player data. If this persists, feel free to dm me: Moonflower#8861')
            logger.exception(e)




    @commands.command(aliases=['dungeon'])
    async def dungeons(self, ctx, *param):
        data = await checkdungeonplayer(ctx, param)
        if data is None: 
            return
        playerstats = data[1]
        profile = data[0]
        playername = data[2]
        playeruuid = data[3]

        # all checks passed
        try:
            dungeonstats = playerstats["members"][playeruuid]["dungeons"]

            levelreq = [50, 125, 235, 395, 625, 955, 1425, 2095, 3045, 4385, 6275, 8940, 12700,
                        17960, 25340, 35640, 50040, 70040, 97640, 135640, 188140, 259640, 356640,
                        488640, 668640, 911640, 1239640, 1684640, 2284640, 3084640, 4149640, 5559640,
                        7459640, 9959640, 13259640, 17559640, 23159640, 30359640, 39559640, 51559640,
                        66559640, 85559640, 109559640, 139559640, 177559640, 225559640, 285559640,
                        360559640, 453559640]

            # get dungeon type data
            type_data = {}
            dungeontypes = dungeonstats["dungeon_types"]
            for dungeontype in dungeontypes:
                totalxp = dungeontypes[dungeontype]["experience"]
                levels = 0
                xp_needed = 50
                progress = 0
                for level in range(len(levelreq)):
                    if totalxp < levelreq[level]:
                        levels = level
                        xp_needed = round(levelreq[level] - totalxp)
                        if level != 0:
                            level_xp = levelreq[level] - levelreq[level - 1]
                        else:
                            level_xp = 50
                        progress = round((level_xp - xp_needed) / level_xp, 2)
                        xp_needed = price_formatter(xp_needed)
                        break
                totalxp = price_formatter(round(totalxp))

                type_data[dungeontype] = {
                    "level": levels,
                    "total": totalxp,
                    "progress_bar": '',
                    "progress": progress,
                    "xp_needed": xp_needed
                }

                if type_data[dungeontype]["xp_needed"] == '0':
                    progressbar = "[====maxed====]"
                else:
                    progressbar = '['
                    equals = round(type_data[dungeontype]["progress"] / (1 / 12))
                    dashes = 12 - equals
                    progressbar = progressbar + equals * '=' + '|' + dashes * '-' + ']'
                type_data[dungeontype]["progress_bar"] = progressbar

            # get class data
            class_data = {}
            classlevels = dungeonstats["player_classes"]
            for dungeon_class in classlevels:
                totalxp = classlevels[dungeon_class]["experience"]
                levels = 0
                xp_needed = 50
                progress = 0
                for level in range(len(levelreq)):
                    if totalxp < levelreq[level]:
                        levels = level
                        xp_needed = round(levelreq[level] - totalxp)
                        if level != 0:
                            level_xp = levelreq[level] - levelreq[level - 1]
                        else:
                            level_xp = 50
                        progress = round((level_xp - xp_needed) / level_xp, 2)
                        xp_needed = price_formatter(xp_needed)
                        break
                totalxp = price_formatter(round(totalxp))

                class_data[dungeon_class] = {
                    "level": levels,
                    "total": totalxp,
                    "progress_bar": '',
                    "progress": progress,
                    "xp_needed": xp_needed
                }

                if class_data[dungeon_class]["xp_needed"] == '0':
                    progressbar = "[====maxed====]"
                else:
                    progressbar = '['
                    equals = round(class_data[dungeon_class]["progress"] / (1 / 12))
                    dashes = 12 - equals
                    progressbar = progressbar + equals * '=' + '|' + dashes * '-' + ']'
                class_data[dungeon_class]["progress_bar"] = progressbar

            embed = discord.Embed(
                title=f"{playername}'s Dungeon Stats",
                color=0xf00000,
                description=f"Data taken from profile: {profile}"
            )

            embed.add_field(
                name=str('☠️️ Catacombs Level ' + str(type_data["catacombs"]["level"])),
                value=str('`' + type_data["catacombs"]["progress_bar"] + '`' +
                          str(int(type_data["catacombs"]["progress"] * 100)) + '%' +
                          "\nTotal XP: " + type_data["catacombs"]["total"] +
                          '\nNext Level: ' + type_data["catacombs"]["xp_needed"] + 'XP'),
                inline=True
            )

            embed.add_field(
                name=str('🚑 Healer Level ' + str(class_data["healer"]["level"])),
                value=str('`' + class_data["healer"]["progress_bar"] + '`' +
                          str(int(class_data["healer"]["progress"] * 100)) + '%' +
                          "\nTotal XP: " + class_data["healer"]["total"] +
                          '\nNext Level: ' + class_data["healer"]["xp_needed"] + 'XP'),
                inline=True
            )
            embed.add_field(
                name=str('🔮️ Mage Level ' + str(class_data["mage"]["level"])),
                value=str('`' + class_data["mage"]["progress_bar"] + '`' +
                          str(int(class_data["mage"]["progress"] * 100)) + '%' +
                          "\nTotal XP: " + class_data["mage"]["total"] +
                          '\nNext Level: ' + class_data["mage"]["xp_needed"] + 'XP'),
                inline=True
            )
            embed.add_field(
                name=str('⚔️ Berserk Level ' + str(class_data["berserk"]["level"])),
                value=str('`' + class_data["berserk"]["progress_bar"] + '`' +
                          str(int(class_data["berserk"]["progress"] * 100)) + '%' +
                          "\nTotal XP: " + class_data["berserk"]["total"] +
                          '\nNext Level: ' + class_data["berserk"]["xp_needed"] + 'XP'),
                inline=True
            )
            embed.add_field(
                name=str('🏹️ Archer Level ' + str(class_data["archer"]["level"])),
                value=str('`' + class_data["archer"]["progress_bar"] + '`' +
                          str(int(class_data["archer"]["progress"] * 100)) + '%' +
                          "\nTotal XP: " + class_data["archer"]["total"] +
                          '\nNext Level: ' + class_data["archer"]["xp_needed"] + 'XP'),
                inline=True
            )
            embed.add_field(
                name=str('🛡️ Tank Level ' + str(class_data["tank"]["level"])),
                value=str('`' + class_data["tank"]["progress_bar"] + '`' +
                          str(int(class_data["tank"]["progress"] * 100)) + '%' +
                          "\nTotal XP: " + class_data["tank"]["total"] +
                          '\nNext Level: ' + class_data["tank"]["xp_needed"] + 'XP'),
                inline=True
            )

            embed.set_thumbnail(url=f"https://crafatar.com/avatars/{playeruuid}?size=40&default=MHF_Steve&overlay.png")
            embed.add_field(
                name="** **",
                value="Also try: `j.skills`, `j.accessories`, `j.armor`, `j.inventory`, `j.auctions`",
                inline=False
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'Error getting player data: Player has no dungeon data on profile {profile}.')
            logger.exception(e)
            return




    @commands.command(aliases=["ah"])
    async def auctions(self, ctx, username):
        mcdata = await checkusername(username)
        if mcdata == -1:
            await ctx.send('Please enter a valid username after .auctions')
            return
        uuid = mcdata[1]
        username = mcdata[0]

        data = getauctiondata()
        if data == {}:
            await ctx.send("Jerry is in the middle of an automatic reboot. Please try again in a few minutes. Thanks!")
            return
        if uuid in data:
            userauctions = data[uuid]
            for item in userauctions:
                # format time til end
                end = datetime.fromtimestamp(int(str(item["end"])[:-3]))
                endingin = end - datetime.now()
                timetilend = str(endingin).split(' ')
                if len(timetilend) > 1:
                    daystilend = int(timetilend[0])
                else:
                    daystilend = 0
                if daystilend < 0:
                    item["endingin"] = 'Ended!'
                else:
                    hourstilend = int(timetilend[-1].split(':')[0])
                    minstilend = int(timetilend[-1].split(':')[1])
                    hourstilend += daystilend * 24
                    item["endingin"] = str(hourstilend) + 'h ' + str(minstilend) + 'm'

            # make the embed
            embed = discord.Embed(title=username + "'s Auctions", color=0xf00000)
            for item in userauctions:
                itemname = item["item_name"]
                startingbid = price_formatter(item["starting_bid"])
                highestbid = price_formatter(item["highest_bid"])
                tier = item["tier"].capitalize()
                endingin = item["endingin"]

                if not item["bin"]:
                    embed.add_field(
                        name=itemname,
                        value=f"Tier: {tier} \nStarting Bid: {startingbid} \nHighest Bid: {highestbid} \nEnds In: {endingin}",
                        inline=False)
                else:
                    embed.add_field(
                        name=itemname,
                        value=f"Tier: {tier} \nBIN: {startingbid} \nEnds In: {endingin}",
                        inline=False)
            embed.set_footer(text="Showing " + str(len(userauctions)) + " ongoing auctions")
            embed.set_thumbnail(url=f"https://crafatar.com/avatars/{uuid}?size=500&default=MHF_Steve&overlay.png")
            embed.add_field(
                name="** **",
                value="Also try: `j.skills`, `j.accessories`, `j.armor`, `j.inventory`, `j.dungeons`",
                inline=False
            )

        else:
            embed = discord.Embed(title=username + "'s Auctions", color=0xf00000)
            embed.set_footer(text="No ongoing auctions found")
        await ctx.send(embed=embed)




    @commands.command(aliases=['bin'])
    async def lowestbin(self, ctx, *itemname):
        itemname = ' '.join(itemname).lower()
        logger.info(f"Finding lowest BIN for {itemname}.")
        with open('auction/bindata.json', 'r') as b:
            bins = json.load(b)
        if bins == {}:
            await ctx.send("Jerry is in the middle of an automatic reboot. Please try again in a few minutes. Thanks!")
            return

        lowestbins = {}
        for item in bins:
            # check item name
            if itemname.lower() in item.lower():
                for auction in bins[item]:
                    # check if it's the lowest price for its rarity
                    rarity = auction["tier"]
                    if rarity not in lowestbins:
                        lowestbins[rarity] = {}
                        lowest = {}
                        lowest["price"] = auction["starting_bid"]
                        lowest["auctioneer"] = auction["auctioneer"]
                        lowestbins[rarity] = lowest
                    else:
                        if auction["starting_bid"] < lowestbins[rarity]["price"]:
                            lowest = {}
                            lowest["price"] = auction["starting_bid"]
                            lowest["auctioneer"] = auction["auctioneer"]
                            lowestbins[rarity] = lowest


        if lowestbins != {}:
            embed = discord.Embed(title="Lowest BIN Prices", color=0xf00000)
            embed.set_footer(text=f"keyword = {itemname}")
            for rarity in lowestbins:
                rarity2 = rarity[0].upper() + rarity[1:]
                embed.add_field(
                    name=rarity2,
                    value=(str(await checkusername(lowestbins[rarity]["auctioneer"])[1]) + '\n' + (price_formatter(lowestbins[rarity]["price"])) + ' coins'
                           ),
                    inline=False
                )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'No BINs found with keyword {itemname}.')




    @commands.command(aliases=['bz'])   
    async def bazaar(self, ctx, *itemname):
        try:
            with open('bazaar/bazaardata.json') as f:
                data = json.load(f)
            if data == {}:
                await ctx.send("Jerry is in the middle of an automatic reboot. Please try again in a few minutes. Thanks!")
                return
            itemname = '_'.join(itemname).upper()
            if itemname not in data:
                found = False
                for name in data:
                    if itemname in name:
                        itemname = name
                        found = True
                if found is False:
                    await ctx.send("Item is not in the bazaar data. Try checking the spelling.")
                    return
            buy_info = '[1x] ' + bz_price_formatter(round(data[itemname]["buy_price"], 1)) + ' coins'\
                + '\n' + '[10x] ' + bz_price_formatter(round(data[itemname]["buy_price"] * 10, 1)) + ' coins'\
                + '\n' + '[64x] ' + bz_price_formatter(round(data[itemname]["buy_price"] * 64, 1)) + ' coins'
            sell_info = '[1x] ' + bz_price_formatter(round(data[itemname]["sell_price"], 1)) + ' coins'\
                + '\n' + '[10x] ' + bz_price_formatter(round(data[itemname]["sell_price"] * 10, 1)) + ' coins'\
                + '\n' + '[64x] ' + bz_price_formatter(round(data[itemname]["sell_price"] * 64, 1)) + ' coins'
            name = bz_name_formatter(itemname)
            embed = discord.Embed(title=f"Bazaar Data for {name}", color=0xf00000)
            embed.add_field(name=f"Buy Price:", value=buy_info)
            embed.add_field(name=f"Sell Price:", value=sell_info)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send('There was an error fetching bazaar data. Please try again later.')
            logger.exception(e)




def setup(client):
    client.add_cog(Skyblock(client))
