from dotenv import load_dotenv
import os
import discord
import asyncio
from parser import get_last_post, get_last_page_href, thread_en, thread_ru
from datetime import datetime


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = int(os.getenv("USER_ID"))

time = datetime.now().strftime("%d/%m/%Y %H:%M")

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await asyncio.gather(
        compare_data(thread_en, "EN", 600),
        compare_data(thread_ru, "RU", 600)
    )


async def compare_data(thread, forum_lang, interval):
    prev_data = None
    while True:
        current_data = get_last_post(thread)
        if prev_data is not None and current_data == prev_data:
            print(f'{time} {forum_lang} forum data not changed')
        else:
            if prev_data is None or prev_data['message'].lower().startswith('up'):
                print(f'{time} {forum_lang} forum data changed quietly')
                prev_data = current_data
            else:
                print(f'{time} {forum_lang} data changed')
                prev_data = current_data
                await send_to_admin(current_data, thread, forum_lang)
        await asyncio.sleep(interval)


async def send_to_admin(current_data, thread, forum_lang):
    user = client.get_user(USER_ID)
    await user.send(f"A new user from the {forum_lang} forum want to join our guild.\n"
                    f"Nickname: {current_data['username']}\n"
                    f"Message: {current_data['message']}\n"
                    f"Profile link: {current_data['profile_url']}\n"
                    f"Forum link: {get_last_page_href(thread)}"
                    )


if __name__ == '__main__':
    client.run(TOKEN)
