import disnake

client = disnake.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

## ADD SECRET FOR TOKEN!
client.run('OTMwNzgxMzk4NDM0OTkyMTQ15.Yd63ug.dq3SxFX-kUbXjG42d4Lsf4uPIXw')
