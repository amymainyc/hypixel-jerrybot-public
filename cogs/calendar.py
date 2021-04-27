import discord
from discord.ext import commands, tasks
import datetime
from datetime import datetime
import json
from loguru import logger
import asyncio


with open('data/database.json') as d:
    database = json.load(d)


class Calendar(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_calendar.start()



    @commands.command()
    async def setupreminders(self, ctx):
        # check if user is server administrator
        if ctx.message.author.guild_permissions.administrator:
            pass
        else:
            await ctx.send('```You must me a server administrator to use this command.```')

        def whosent(m):
            return m.author == ctx.author

        # get channel
        channel = ctx.channel.id

        with open("data/calendar.json", "r") as f:
            data = json.load(f)

        cal_types = ""
        for event in data:
            cal_types += f"{event}, "
        cal_types += "All of the Above"

        # ask for a caltype and check if it's valid
        await ctx.send("```Please reply with an event type to set up reminders for. \n\n"
        f"Valid types: {cal_types}```")

        async def validcaltype(m):
            msg = m.content
            for event in data:
                if msg.lower() == event.lower():
                    return True
            await ctx.send("```Invalid event type. \nPlease refer to the message above for types of events.```")
            print(msg)
            return False

        try:
            caltypemsg = await self.client.wait_for('message', check=whosent, timeout=60.0)
        except asyncio.TimeoutError:
            return await ctx.send('You took too long \:( Please try the command again.')

        if await validcaltype(caltypemsg):
            pass
        else:
            return

        caltype = caltypemsg.content.lower()

        await self.addreminder(ctx, channel, caltype)
        logger.info(f"Reminders set up for channel {channel}")

    async def addreminder(self, ctx, channel, caltype):
        with open('data/eventchannels.json') as d:
            data = json.load(d)
        caltypekey = caltype.replace(' ', '_')
        caltypekey = ''.join(caltypekey.split("'"))

        if caltypekey not in data:
            data[caltypekey] = []

        if caltypekey == "all_of_the_above":
            added = 0
            for event in data:
                if channel not in data[event]:
                    data[event].append(channel)
                    added += 1
            if added != 0:
                await ctx.send('```Reminders set up for ' + str(added) + ' events in this channel.```')
            else:
                await ctx.send('```Reminders already set up for all events in this channel.```')

        else:
            if channel not in data[caltypekey]:
                data[caltypekey].append(channel)
                await ctx.send('```Reminders set up for ' + caltype + ' in this channel.```')
            else:
                await ctx.send('```Reminders already set up for ' + caltype + ' in this channel.```')

        with open('data/eventchannels.json', 'w') as d:
            json.dump(data, d, indent=4)


    @commands.command()
    async def disablereminders(self, ctx):
        # check if user is server administrator
        if ctx.message.author.guild_permissions.administrator:
            pass
        else:
            await ctx.send('```You must me a server administrator to use this command.```')

        def whosent(m):
            return m.author == ctx.author

        # get channel
        channel = ctx.channel.id

        with open("data/calendar.json", "r") as f:
            data = json.load(f)

        cal_types = ""
        for event in data:
            cal_types += f"{event}, "
        cal_types += "All of the Above"

        # ask for a caltype and check if it's valid
        await ctx.send("```Please reply with an event type to disable reminders for. \n\n"
        f"Valid types: {cal_types}```")

        async def validcaltype(m):
            msg = m.content
            for event in data:
                if msg.lower() == event.lower():
                    return True
            await ctx.send("```Invalid event type. \nPlease refer to the message above for types of events.```")
            print(msg)
            return False

        try:
            caltypemsg = await self.client.wait_for('message', check=whosent, timeout=60.0)
        except asyncio.TimeoutError:
            return await ctx.send('You took too long \:( Please try the command again.')

        if await validcaltype(caltypemsg):
            pass
        else:
            return

        caltype = caltypemsg.content.lower()

        await self.removereminder(ctx, channel, caltype)
        logger.info(f"Reminders disabled for channel {channel}")

    async def removereminder(self, ctx, channel, caltype):
        with open('data/eventchannels.json') as d:
            data = json.load(d)
        caltypekey = caltype.replace(' ', '_')
        caltypekey = ''.join(caltypekey.split("'"))

        if caltypekey == "all_of_the_above":
            added = 0
            for event in data:
                if channel in data[event]:
                    data[event].remove(channel)
                    added += 1
            if added != 0:
                await ctx.send('```Reminders disabled for ' + str(added) + ' events in this channel.```')
            else:
                await ctx.send('```Reminders already disabled for all events in this channel.```')

        else:
            if channel in data[caltypekey]:
                data[caltypekey].remove(channel)
                await ctx.send('```Reminders disabled for ' + caltype + ' in this channel.```')
            else:
                await ctx.send('```Reminders already disabled for ' + caltype + ' in this channel.```')

        with open('data/eventchannels.json', 'w') as d:
            json.dump(data, d, indent=4)



    @tasks.loop(seconds=10)
    async def check_calendar(self):
        try:
            # check if it is time
            with open("data/calendar.json", "r") as f:
                data = json.load(f)

            next_events = []
            for event in data:
                time = data[event]["time"]
                intervals = data[event]["intervals"]
                iterations = data[event]["iterations"]
                if iterations == 0:
                    if abs(int(datetime.utcnow().timestamp()) - time) < 120:
                        next_events.insert(0, event)
                elif iterations > 0:
                    if abs(int(datetime.utcnow().timestamp()) - time) // intervals < iterations:
                        if abs(int(datetime.utcnow().timestamp()) - time) % intervals < 120:
                            next_events.insert(0, event)
                else:
                    if abs(int(datetime.utcnow().timestamp()) - time) % intervals < 120:
                        next_events.insert(0, event)

            if next_events == []:
                return
            logger.info(f"Event: {next_events}")
            
            messages = []
            for event in next_events:
                # get channels
                with open("data/eventchannels.json", "r") as f:
                    eventchannels = json.load(f)

                key = event.lower()
                key = key.replace(" ", "_")
                key = key.replace("'", "")

                channels = eventchannels[key]

                emoji1 = data[event]["emojis"][0]
                emoji2 = data[event]["emojis"][1]
                color = discord.Color(int(data[event]["color"], 16))
                title = f"{emoji1} {event} {emoji2}"
                embed_field_name = "Time until event starts:"
                embed_field_text = "2 minutes"
                footer = "j.help | bit.ly/jerrys-skyblock"

                embed = discord.Embed(title=title, color=color)
                embed.add_field(name=embed_field_name, value=embed_field_text)
                embed.set_footer(text=footer)

                for channel in channels:
                    try:
                        channel = self.client.get_channel(channel)
                        messages.insert(0, await channel.send(embed=embed))
                    except Exception as e:
                        logger.exception(e)

            await asyncio.sleep(60)
            for message in messages:
                try:
                    embed = message.embeds[0]
                    embed.clear_fields
                    embed.set_field_at(0, name=embed_field_name, value="1 minute")
                    await message.edit(embed=embed)
                except Exception as e:
                    logger.exception(e)
            await asyncio.sleep(60)
            for message in messages:
                try:
                    embed = message.embeds[0]
                    embed.clear_fields
                    embed.set_field_at(0, name=embed_field_name, value="Event Started!")
                    await message.edit(embed=embed)
                except Exception as e:
                    logger.exception(e)
            await asyncio.sleep(120)
            
        except Exception as e:
            logger.exception(e)


    
    @commands.command()
    async def add_event(self, ctx, name, emoji1, emoji2, first_time, intervals, iterations, color):
        if ctx.author != self.client.get_user(430079880353546242):
            return
        with open("data/calendar.json", "r") as f:
            data = json.load(f)

        event = {
            "time": int(first_time),
            "emojis": [emoji1, emoji2],
            "intervals": int(intervals),
            "iterations": int(iterations),
            "color": color
        }

        first_time = str(datetime.utcfromtimestamp(int(first_time)))
        
        await ctx.send(
            f"```Event: {name}\n"
            f"Emojis: {emoji1}, {emoji2}\n"
            f"Time: {first_time}\n"
            f"Intervals: {intervals}\n"
            f"Iterations: {iterations}\n"
            f"Color: {color}```"
            f"Is that correct?"
        )

        def whosent(m):
            return m.author == ctx.author

        async def confirmation(m):
            if m.author == ctx.author:
                if m.content.lower() == "yes":
                    return True
                else:
                    await ctx.send("```Cancelling event creation.```")
                    return False

        try:
            message = await self.client.wait_for('message', check=whosent, timeout=60.0)
        except asyncio.TimeoutError:
            return await ctx.send('You took too long \:( Please try the command again.')

        if await confirmation(message):
            pass
        else:
            return

        data[name] = event

        with open("data/calendar.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"```Event: {name} created.```")

        



def setup(client):
    client.add_cog(Calendar(client))
