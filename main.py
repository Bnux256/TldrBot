import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os
import lib.tldr_cli as tldr_cli
import lib.progress_bar as progress_bar
import lib.md_parser as md_parser

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
    param user_input(str): current input
    returns [str]: languages that begin with the commands' letters
    """
    # Discord doesn't allow for autocomplete larger than 25 therefore we return the first 25 languages
    if not user_input:
        languages = tldr_cli.get_languages()
        return languages[len(languages)-25:]  # returning the last 25 languages
    else:
        return [lang for lang in tldr_cli.get_languages() if user_input.lower() in lang]


@bot.slash_command(description="Retrieve the TLDR for a command")
async def tldr(
        inter: disnake.ApplicationCommandInteraction,
        command: str,
        # platform: str = commands.Param(choices=tldr_cli.get_platforms()),
        platform: str = commands.Param(default="common",choices=tldr_cli.get_platforms()),
        language: str = commands.Param(default="en", autocomplete=autocomp_langs)
        # language: str = "en" or commands.Param(autocomplete=autocomp_langs)
):
    print('User Entered: tldr %s (platform: %s; language: %s)' % (command, platform, (language or 'en')))

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

    # if command exists we send it
    else:
        embed: disnake.Embed() = md_parser.md_to_embed(md)

    await inter.send(embed=embed)  # sending the embed


try:
    bot.run(TOKEN)
except Exception as e:
    print(e)
