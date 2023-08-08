import os
from dotenv import load_dotenv
import discord
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID=int(os.getenv('GUILD_ID'))
GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))
WELCOME_CHANNEL=int(os.getenv('GENERAL'))
WEBHOOK_URL_1=os.getenv('WEBHOOK_URL_1')
DB_PASS=os.getenv('DB_PASS')