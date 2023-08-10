import discord
from discord.ext import commands
from settings import TOKEN,GUILD,GUILD_ID,cursor,commit

def run():
    try:
        intents=discord.Intents.default()
        intents.members=True
        intents.message_content=True

        bot = commands.Bot(command_prefix='!', intents=intents)

        @bot.event
        async def on_ready():   
            print(f"User: {bot.user.name} (ID: {bot.user.id})")
            await bot.load_extension('cogs.JoinParty')
            await bot.load_extension('cogs.NewRoleChannel')
            await bot.load_extension('slashcmds.sync')
            bot.tree.copy_global_to(guild=GUILD)
            await bot.tree.sync(guild=GUILD)
            
        bot.run(TOKEN)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    run()