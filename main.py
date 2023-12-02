from decouple import config
import discord
from discord.ext import commands
import json
import requests

from test_data import data
lb_data = data

session_cookie=config('session_cookie')
url=config('url')
discord_token=config('discord_token')
discord_guild=int(config('discord_guild'))
discord_channel1=int(config('discord_channel1'))
discord_channel2=int(config('discord_channel2'))
discord_channel3=int(config('discord_channel3'))

# lb_data = {}
cookie = {'session': session_cookie}

def save_to_file(filename, variable, name):
    file1 = open(filename, "w", encoding="utf-8")
    file1.write(f"{name} = ")  # + str(variable).encode('utf8'))
    file1.write(str(variable))
    file1.close()
    print(f"Saved as {filename}")


intents = discord.Intents.default()
# intents.message_content = True
client = discord.Client(intents=intents)
# client=commands.Bot(intents=intents, command_prefix="!")

@ client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
#     guild = client.get_guild(discord_guild)
#     if not guild:
#         print("Guild not found!")
#         return
#     voice_channel = guild.get_channel(discord_channel1)
#     if not voice_channel:
#         print("Voice channel not found!")
#         return
#     await voice_channel.edit(name="Test")
# @client.command(name='change_vc_name')
# async def change_vc_name(ctx, *, new_name: str):
#     guild = client.get_guild(discord_guild)
#     if not guild:
#         print("Guild not found!")
#         return
#     voice_channel = guild.get_channel(discord_channel1)
#     if not voice_channel:
#         print("Voice channel not found!")
#         return
#     await voice_channel.edit(name="Test")


@ client.event
async def on_message(message):
    # print(message.content)
    # print(dir(message))
    guild = client.get_guild(discord_guild)
    print(guild)
    if not guild:
        print("Guild not found!")
        return
    voice_channel = guild.get_channel(discord_channel1)
    if not voice_channel:
        print("Voice channel not found!")
        return
    await voice_channel.edit(name="Test")
    # if(message.)

def fetch_leaderboard():
    response = requests.get(
        url,
        timeout=60,
        cookies=cookie
        )


    if response.status_code == 200:
        # Parse the JSON data into a dictionary
        lb_data = response.json()
        # lb_data = data
        # Now, `data` is a Python dictionary containing the JSON data
        # print(data)
        # save_to_file("test_data.py", lb_data, "data")
    else:
        print("Failed to fetch data: HTTP Status Code", response.status_code)


client.run(discord_token)
