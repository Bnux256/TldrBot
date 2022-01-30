import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.join(os.getcwd(), r'tldr'))
import tldr

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
    print()

    
@bot.slash_command(description="Update the bot's TLDR Pages cache")
async def update(inter):
    await inter.response.send_message(tldr.update_cache())

    
@bot.slash_command(description="Retrieve the TLDR for a command")
async def tldr(inter, command, platform: str = "common", language: str = "None"):
    await inter.response.send_message(tldr.get_md(command, platform, language))

try:
    bot.run(TOKEN)
except Exception as e:
    print(e)