import asyncio
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os
import sys
import tldr.tldr as tldr

load_dotenv()  # Loading env variables from .env file
TOKEN = os.getenv('TOKEN')  # Setting environment variable as const

bot = commands.Bot(
    command_prefix=">",
    test_guilds=[866375498762551317]
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

    
@bot.slash_command(description="Update the bot's TLDR Pages cache")
async def update(inter):
    await asyncio.run(tldr.update_cache())
    await inter.response.send_message('Cache updated!')

# test
@bot.slash_command(description="Responds with 'World'")
async def hello(inter, command):
    await inter.response.send_message(hello(command))

def hello(command):
    print('aaa')
    return tldr.get_md(command)
#test     

@bot.slash_command(description="Retrieve the TLDR for a command")
async def tldr(inter, command, platform: str = "common", language: str = "None"):
    await inter.response.send_message(tldr.get_md(command, platform, language))

try:
    bot.run(TOKEN)
except Exception as e:
    print(e)