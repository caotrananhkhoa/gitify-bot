import random
import discord
from discord.ext import commands

MAX_GUESS = 3

class PlusGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("PlusGame is ready!")

    @commands.command()
    async def playPlusGame(self, ctx, *args):
        try:
            # Check the sender is not bot
            if (ctx.author == self.bot.user):
                return

            def check(message):
                return message.author == ctx.author and message.channel == ctx.message.channel
            
            await ctx.send('Welcome to Plus Game!')

            if (len(args) == 0):
                numberA = random.randint(1, 100)
                numberB = random.randint(1, 100)

                answer = numberA + numberB
                await ctx.send('{} + {} = ?'.format(str(numberA), str(numberB)))
                count = 0
                while count < MAX_GUESS:
                    message = await self.bot.wait_for("message", check=check)
                    
                    if (message.content.isdigit() == False):
                        await ctx.send("Please send a integer number")

                    elif (message.content == str(answer)):
                        await ctx.send("Correct! It took you {} tries".format(str(count + 1)))
                        return
                    
                    elif (count < MAX_GUESS - 1):
                        await ctx.send("Incorrect! You have {} tries remain".format(str(MAX_GUESS - count - 1)))
                        count = count + 1

                    elif (count == MAX_GUESS - 1):
                        await ctx.send("You don't have any tries! The answer is **{}**".format(str(answer)))
                        count = count + 1
                    
            elif (args[0] == "h"):
                await ctx.send("""You will receive a Plus Expression and try to send the correct solution.""")
        
        except Exception as e:
            await ctx.send(e)
        




async def setup(bot):
    await bot.add_cog(PlusGame(bot))
