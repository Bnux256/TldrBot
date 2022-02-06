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
    await asyncio.run(tldr_cli.update_cache())
    await inter.response.send_message('Cache updated!')


# test
@bot.slash_command(description="Responds with 'World'")
async def hello(inter, command):
    '''
    loop = asyncio.get_event_loop()
    result = tldr.temp()
    future = asyncio.run_coroutine_threadsafe(result, loop)
    print(future)
    '''
    #future = asyncio.run(tldr.temp())
    #await tldr.temp.run(inter)
    value = tldr_cli.get_md('cd')
    await inter.response.send_message(value)


# test

@bot.slash_command(description="Retrieve the TLDR for a command")
async def tldr(inter, command, platform: str = "common", language: str = None):
    print('command, platform, laguage:', command, platform, language)
    md = tldr_cli.get_md(command, platform, language)
    await inter.response.send_message(md)


try:
    bot.run(TOKEN)
except Exception as e:
    print(e)