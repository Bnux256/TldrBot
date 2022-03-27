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
    description: str = ""
    fields: [[str]] = []
    field: [str] = []
    title: str = ""

    # going through the lines of file
    for line in lines:

        # parsing header lines
        if "#" in line and not ("##" in line):
            title = line[line.find("#") + 1:]

        # parsing description lines
        if ">" in line:
            description += line[line.find(">") + 1:]

        # parsing field lines
        if line.startswith("-") or line.startswith(" -"):
            field: [str] = [line[line.find("-"):]]

        # parsing back tick code lines
        if line.startswith("`") or line.startswith(" `"):
            field.append(line[line.find("`"):])
            fields.append(field)

    # creating embed
    embed = disnake.Embed(title=title, colour=disnake.Colour.from_rgb(54, 57, 63), description=description)

    # adding all fields to embed
    for field in fields:
        embed.add_field(field[0], field[1], inline=False)

    return embed
