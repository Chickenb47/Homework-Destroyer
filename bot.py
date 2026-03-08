import discord
import aiohttp
import os

TOKEN = os.environ['DISCORD_TOKEN']
WEBHOOK_URL = os.environ['N8N_WEBHOOK_URL']

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot is online as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    payload = {
        'content': message.content,
        'author': str(message.author),
        'channel': str(message.channel),
        'attachments': [a.url for a in message.attachments]
    }

    async with aiohttp.ClientSession() as session:
        await session.post(WEBHOOK_URL, json=payload)

client.run(TOKEN)
