import discord
from discord.ext import commands, tasks
import requests
import json
import asyncio

bot_token = "MTI3MzAyODQ2OTc4OTI5NDcwMw.GgyeIw.3ELSs4z3hxoHrgPkkNHV6RN24UM_lvI4Z1m6Is"

client_id = "b8jk0k9u00u5fegxq58sv4ul9r3lz3"
client_secret = "7g9bd9yyr5l5hxpi5kt6ibky9y1l9o"

channel_id = 1273027312539009066

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def check_stream():
    while True:
        print("Checking if stream is live...")
        print("Generating Twitch token...")
        response = requests.post(
            "https://id.twitch.tv/oauth2/token",
            params={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials"
            }
        )
        print("Twitch token response:", response.text)
        print("Twitch token generated.")
        print("Access token:", response.json()["access_token"])
        access_token = response.json()["access_token"]
        print("Checking if Aduritebh is live...")
        url = f"https://api.twitch.tv/helix/streams?user_login=aduuritetbh"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-ID": client_id
        }
        response = requests.get(url, headers=headers)
        print("Response status code:", response.status_code)
        print("Response text:", response.text)
        if response.status_code == 200:
            print("Response is OK.")
            data = json.loads(response.text)
            print("Data:", data)
            if not data["data"]:
                print("Stream is not live. Waiting 5 seconds before checking again...")
                await asyncio.sleep(5)
                print("Checking again...")
                channel = bot.get_channel(channel_id)
                print(f"Channel object: {channel}")
                print(f"Sending message to channel {channel.name}...")
                await channel.send("Aduritebh is not live. Checking again soon!")
                print("Message sent!")
            else:
                for stream in data["data"]:
                    print("Stream type:", stream["type"])
                    if stream["type"] == "live":
                        print("Stream is live!")
                        channel = bot.get_channel(channel_id)
                        print(f"Channel object: {channel}")
                        print(f"Sending message to channel {channel.name}...")
                        await channel.send("Aduritebh is live! https://www.twitch.tv/aduuritetbh")
                        print("Message sent!")
        else:
            print("Response is not OK.")
        print("Waiting 10 seconds before checking again...")
        await asyncio.sleep(10)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    print("Bot guilds:", bot.guilds)
    asyncio.create_task(check_stream())

bot.run(bot_token)
