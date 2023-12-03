from decouple import config

import discord
from discord.ext import commands
import json
import requests
from time import sleep as sl

def sleep(seconds):
    print(f"Sleeping for {seconds} seconds")
    sl(seconds)

session_cookie=config('session_cookie')
cookie = {'session': session_cookie}
url=config('url')
discord_token=config('discord_token')
discord_guild=int(config('discord_guild'))
discord_channels = []
discord_channels.append(int(config('discord_channel1')))
discord_channels.append(int(config('discord_channel2')))
discord_channels.append(int(config('discord_channel3')))



async def get_sorted_leaderboard():

    data = await fetch_leaderboard()
    sorted_list = sorted(
        ((value['local_score'], value['name']) for key, value in data['members'].items()),
        reverse=True
    )
    print(sorted_list)
    sorted_names = [name for score, name in sorted_list]
    sorted_scores = [score for score, name in sorted_list]
    print(sorted_names)
    print(sorted_scores)
    leaderboard = []
    for i in range(0,3):
        leaderboard.append(f"{sorted_scores[i]}⭐ {sorted_names[i]}")
    print(leaderboard)
    return leaderboard


intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def change_vc(channel, new_name):
    guild = client.get_guild(discord_guild)
    if not guild:
        print("Guild not found!")
        return
    voice_channel = guild.get_channel(channel)
    if not voice_channel:
        print("Voice channel not found!")
        return
    await voice_channel.edit(name=new_name)



@ client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    i = 0
    while True:
        sorted_data = await get_sorted_leaderboard()
        for i in range(0,3):
            await change_vc(discord_channels[i], sorted_data[i])
            print(f"Updated channel {i} to {sorted_data[i]}")
            sleep(1)
        sleep(60 * 15)

async def fetch_leaderboard():
    print("Fetching new leaderboard data")
    response = requests.get(
        url,
        timeout=60,
        cookies=cookie
        )

    if response.status_code == 200:
        lb_data = response.json()
        return lb_data
    else:
        print("Failed to fetch data: HTTP Status Code", response.status_code)
    return None

client.run(discord_token)