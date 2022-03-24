import asyncio
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os
import sys
import lib.tldr_cli as tldr_cli
import lib.progress_bar as progress_bar

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
async def update(inter: disnake.ApplicationCommandInteraction):
    # setting gens
    update_gen = tldr_cli.update_cache()
    progress_gen = progress_bar.progress_bar(4)

    # creating embed
    embed = disnake.Embed(colour=disnake.Colour.from_rgb(54,57,63))
    embed.add_field(next(progress_gen), next(update_gen))
    embed.set_author(name = "Updating Cache", icon_url = "https://cdn.discordapp.com/emojis/936226298429329489.gif?size=44&quality=lossless")
    await inter.send(embed = embed)

    # updating progress
    for i in range(4):
        embed.clear_fields()
        embed.add_field(next(progress_gen), next(update_gen))
        await inter.edit_original_message(embed = embed)
    
    # sending finished embed
    embed.clear_fields()
    embed.set_author(name = "Cache Updated!", icon_url = "https://cdn.discordapp.com/emojis/949338159538384926.webp?size=96&quality=lossless")
    await inter.edit_original_message(embed = embed)

async def autocomp_langs(inter: disnake.ApplicationCommandInteraction, user_input: str):
    return [lang for lang in tldr_cli.get_languages() if user_input.lower() in lang]

@bot.slash_command(description="Retrieve the TLDR for a command")
async def tldr(
    inter: disnake.ApplicationCommandInteraction,
    command: str,
    platform: str = commands.Param(choices=tldr_cli.get_platforms()),
    language: str = None
    #language: str = commands.Param(autocomplete=autocomp_langs)
    ):

    print('User Entered: tldr %s (platform: %s; language: %s)' % (command, platform, (language or 'en')))
    md = tldr_cli.get_md(command, platform, language)
    
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