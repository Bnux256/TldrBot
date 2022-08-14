import os
import logging

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

import lib.md_parser as md_parser
import lib.progress_bar as progress_bar
import lib.tldr_cli as tldr_cli

# if TOKEN env var isn't None than we're running from docker
if not os.getenv('TOKEN'):
    load_dotenv()  # Loading env variables from .env file
TOKEN = os.getenv('TOKEN')  # Setting environment variable as const

bot = commands.InteractionBot()

log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'
logging.basicConfig(level='INFO', format=log_format)
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"The server is on {len(bot.guilds)} servers!")
    print("-------")

@bot.slash_command(description="Update the bot's TLDR Pages cache")
async def update(inter: disnake.ApplicationCommandInteraction):
    # setting gens
    update_gen = tldr_cli.update_cache()
    progress_gen = progress_bar.progress_bar(4)

    # creating embed
    embed = disnake.Embed(colour=disnake.Colour.from_rgb(54, 57, 63))
    embed.add_field(next(progress_gen), next(update_gen))
    embed.set_author(name="Updating Cache",
                     icon_url="https://cdn.discordapp.com/emojis/936226298429329489.gif?size=44&quality=lossless")
    await inter.send(embed=embed)

    # updating progress
    for i in range(4):
        embed.clear_fields()
        embed.add_field(next(progress_gen), next(update_gen))
        await inter.edit_original_message(embed=embed)

    # sending finished embed
    embed.clear_fields()
    embed.set_author(name="Cache Updated!",
                     icon_url="https://cdn.discordapp.com/emojis/949338159538384926.webp?size=96&quality=lossless")
    await inter.edit_original_message(embed=embed)


async def autocomp_langs(inter: disnake.ApplicationCommandInteraction, user_input: str):
    """
    autocomplete function for languages
    param: user_input(str): current input
    returns [str]: languages that begin with the given input
    """
    # Discord doesn't allow for autocomplete larger than 25 therefore we return the first 25 languages
    languages = sorted([lang for lang in tldr_cli.get_languages() if lang.lower().startswith(user_input.lower())])
    # returning the last 25 languages
    if len(languages) > 25:
        return languages[:24]
    else:
        return languages 

async def autocomp_platform(inter: disnake.ApplicationCommandInteraction, user_input: str):
    """
    autocomplete for chosing platform
    param: user_input(str): current input
    returns [str]: platform that begin with the given input
    """
    platforms = [platform for platform in tldr_cli.get_platforms() if platform.lower().startswith(user_input.lower())]
    if len(platforms) > 25:
        return platforms[:24]
    else:
        return platforms 


async def autocomp_command(inter: disnake.ApplicationCommandInteraction, user_input: str):
    """
    autocomplete for chosing the command
    param: user_input(str): current input
    returns [str]: commands that begin with the given input
    """
    commands = [command for command in tldr_cli.get_commands() if command.lower().startswith(user_input.lower())]
    if len(commands) > 25:
        return commands[:24]
    else:
        return commands

@bot.slash_command(description="Retrieve the TLDR for a command")
async def tldr(
        inter: disnake.ApplicationCommandInteraction,
        command: str = commands.Param(autocomplete=autocomp_command, description="Choose a command!"),
        platform: str = commands.Param(default="common", autocomplete=autocomp_platform, description="optional - default: common - choose the platform you need"),
        language: str = commands.Param(default="en", autocomplete=autocomp_langs, description="optional - default: english - choose the prefered language")
):
    logging.info('User Entered: tldr %s (platform: %s; language: %s)' % (command, platform, (language or 'en')))

    # if language is english we treat it as None
    if language == 'en':
        md = tldr_cli.get_md(command, platform)
    else:
        md = tldr_cli.get_md(command, platform, language)

    # if command doesn't exist we notify user
    if md is None:
        error_msg: str = "Command doesn't exist in cache. To update, run `/update` command."
        embed: disnake.Embed() = disnake.Embed(description=error_msg, colour=disnake.Colour.from_rgb(237, 66, 69))
        embed.set_author(name="Error", icon_url="https://images-ext-2.discordapp.net/external/6HgbQ8ajjgJozMXg37BWe53K5YTN3YMVmWC93ioekY8/https/raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f6ab.png")
        
        # telling user if command exists in other platforms
        for cur_platform in tldr_cli.get_platforms():
            if tldr_cli.is_in_cache(command, platform=cur_platform):
                embed.add_field(name="This command exists in " + cur_platform, value="You can run: `/tldr command:" + command + " platform: " + cur_platform + "`")

    # if command exists we send it
    else:
        embed: disnake.Embed() = md_parser.md_to_embed(md)

    await inter.send(embed=embed)  # sending the embed


bot.run(TOKEN)