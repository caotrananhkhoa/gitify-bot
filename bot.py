import sys

import discord
from discord.ext import commands

# Add "Game" directory
sys.path.append("Game")

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="!")

@bot.event
async def on_ready():
    print('We have logged in as {} \n'.format(bot.user))
    print('The list of guild: {} \n'.format(', '.join(str(item) for item in bot.guilds)))
    await bot.load_extension("plusGame")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

def run(token):
    bot.run(token)