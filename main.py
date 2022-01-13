import os

import disnake
from dotenv import load_dotenv
import os

load_dotenv()  # Loading env variables from .env file
TOKEN = os.getenv('TOKEN')

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


client.run(TOKEN)
