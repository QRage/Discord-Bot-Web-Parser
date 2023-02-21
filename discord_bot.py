from dotenv import load_dotenv
import os
import discord
from discord.ext import tasks


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

text_chat = client.get_channel(1072880081652953178)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    task_loop.start()


@tasks.loop(seconds=600)
async def task_loop():
    pass


if __name__ == '__main__':
    client.run(TOKEN)
