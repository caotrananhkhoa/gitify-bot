import random
import discord
from discord.ext import commands, tasks
from dataclasses import dataclass
import datetime

# Get region of guild
import geopy
from geopy.geocoders import Nominatim

# Timezone
import pytz
from datetime import datetime

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

session = Session()


MAX_GUESS = 3

class PlusGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("PlusGame is ready!")

    @tasks.loop()
    async def playPlusGame(self, ctx, *args):
        try:
            # Check the sender is not bot
            if (ctx.author == self.bot.user):
                return

            def check(message):
                return message.author == ctx.author and message.channel == ctx.message.channel and ctx.author != self.bot.user

            if (len(args) == 0):
                numberA = random.randint(1, 100)
                numberB = random.randint(1, 100)

                answer = numberA + numberB
                await ctx.send('{} + {} = ?'.format(str(numberA), str(numberB)))
                count = 0
                while count < MAX_GUESS:
                    message = await self.bot.wait_for("message", check=check)
                    
                    if message.content.startswith("!"):
                        return
                    
                    elif (message.content.isdigit() == False):
                        await ctx.send("Please send a integer number")
                        await ctx.send('{} + {} = ?'.format(str(numberA), str(numberB)))

                    elif (message.content == str(answer)):
                        await ctx.send("Correct! It took you {} tries".format(str(count + 1)))
                        return
                    
                    elif (count < MAX_GUESS - 1):
                        await ctx.send("Incorrect! You have {} tries remain".format(str(MAX_GUESS - count - 1)))
                        await ctx.send('{} + {} = ?'.format(str(numberA), str(numberB)))
                        count = count + 1

                    elif (count == MAX_GUESS - 1):
                        await ctx.send("You don't have any tries! The answer is **{}**".format(str(answer)))
                        count = count + 1
                    
            elif (args[0] == "h"):
                await ctx.send("""You will receive a Plus Expression and try to send the correct solution.""")
        
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def startPlusGame(self, ctx, *args):
        # Start a session
        if session.is_active == False:
            session.is_active = True
            session.start_time = ctx.message.created_at.timestamp()
            tz = pytz.timezone('Asia/Ho_Chi_Minh')
            dt = datetime.fromtimestamp(session.start_time, tz)

            # Get the local time in the desired format
            human_readable_time = dt.strftime('%Y-%m-%d, %H:%M:%S')
            await ctx.send('Welcome to Plus Game!')
            await ctx.send(f"The Plus Game session started at {human_readable_time}")
            self.playPlusGame.start(ctx, *args)
        else:
            await ctx.send('A Plus Game session is active!')
            return
    
    @commands.command()
    async def endPlusGame(self, ctx):
        # End a session
        if session.is_active == True:
            session.is_active = False
            session.start_time = ctx.message.created_at.timestamp()
            self.playPlusGame.cancel()
            tz = pytz.timezone('Asia/Ho_Chi_Minh')
            dt = datetime.fromtimestamp(session.start_time, tz)

            # Get the local time in the desired format
            human_readable_time = dt.strftime('%Y-%m-%d, %H:%M:%S')
            await ctx.send('Thanks to play Plus Game!')
            await ctx.send(f"The Plus Game session ended at {human_readable_time}")
            
        else:
            await ctx.send('No Plus Game session is active!')
            return


async def setup(bot):
    await bot.add_cog(PlusGame(bot))
