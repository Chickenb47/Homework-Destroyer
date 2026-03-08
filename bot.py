import discord
import aiohttp
import os

TOKEN = os.environ.get('DISCORD_TOKEN')
WEBHOOK_URL = os.environ.get('N8N_WEBHOOK_URL')

if not TOKEN:
    raise ValueError('DISCORD_TOKEN environment variable is not set')
if not WEBHOOK_URL:
    raise ValueError('N8N_WEBHOOK_URL environment variable is not set')

intents = discord.Intents.default()
intents.message_content = True

session: aiohttp.ClientSession = None
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    global session
    session = aiohttp.ClientSession()
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

    try:
        async with session.post(WEBHOOK_URL, json=payload) as resp:
            if resp.status != 200:
                print(f'Webhook error: {resp.status}')
    except Exception as e:
        print(f'Failed to send to webhook: {e}')

client.run(TOKEN)
