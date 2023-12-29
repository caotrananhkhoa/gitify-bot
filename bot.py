import os
from dotenv import load_dotenv
import random

import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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

bot.run(TOKEN)
