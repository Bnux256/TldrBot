import asyncio
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os
import sys
import tldr_cli.tldr_cli as tldr_cli

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
    tldr_cli.update_cache()
    await inter.response.send_message('Cache updated!')


@bot.slash_command(description="Retrieve the TLDR for a command")
async def tldr(inter, command, platform: str = "common", language: str = None):
    md = tldr_cli.get_md(command, platform, language)
    print('User Entered: tldr %s (platform: %s; language: %s)' % (command, platform, (language or 'en')))

    # if command doesn't exist we will check if it exists in different platforms
    if md is None:
        # add maybe - maybe you meant different platform? in hieracy.
        await inter.response.send_message('Command doesn\'t exist in cache. To update, run /update command.')
    
    # if command exists we send it
    else:
        await inter.response.send_message(md)


try:
    bot.run(TOKEN)
except Exception as e:
    print(e)