import discord
from discord.ext import commands
from settings import TOKEN

def run():
    intents=discord.Intents.default()
    intents.members=True
    intents.message_content=True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f"User: {bot.user.name} (ID: {bot.user.id})")
        await bot.load_extension('cogs.JoinParty')
    bot.run(TOKEN)

if __name__ == "__main__":
    run()