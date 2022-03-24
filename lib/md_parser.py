import disnake


def md_to_embed(md_command: str):
    """
    The function parses markdown of a command and returns a Discord Embed.
    Params:
    md_commmand (str): a command's markdown file converted to string
    Returns:
    embed (discord.embed?????): An embed that prints the command.
    """
    lines: [str] = md_command.split("\n")
    embed: disnake.Embed() = disnake.Embed(colour=disnake.Colour.from_rgb(54, 57, 63))
    description: str = ""
    field: [str] = []
    # going through the lines of file
    for line in lines:

        # parsing header lines
        if "#" in line and not ("##" in line):
            embed.title(line[line.find("#") + 1:])

        # parsing description lines
        if ">" in line:
            description += line[line.find(">") + 1:]

        # parsing field lines
        if line.startswith("-") or line.startswith(" -"):
            field[0] = line[line.find("-"):]

        # parsing back tick code lines
        if line.startswith("`") or line.startswith(" `"):
            field[1] = line[line.find("`"):]
            embed.add_field(field[0], field[1])

    embed.description(description)
    return embed
