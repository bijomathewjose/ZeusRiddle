from discord.ext import commands
from settings import WELCOME_CHANNEL

class JoinParty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(WELCOME_CHANNEL)
        print(channel)
        if channel:
            await channel.send(f'{member.mention} Welcome to {member.guild.name}')

async def setup(bot):
    await bot.add_cog(JoinParty(bot))