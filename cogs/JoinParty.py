import logging
import discord
from discord.ext import commands
from settings import WELCOME_CHANNEL
from utils.JoinPartyUtil import add_user,message_channel,direct_message_user
from utils.JoinPartyUtil import remove_member_from_db,good_bye_message
from utils import NewRoleChannelUtil

logger = logging.getLogger("bot")
class JoinParty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            await add_user(member)
            await message_channel(self.bot,member,WELCOME_CHANNEL)
            await direct_message_user(member=member)
        except Exception as e:
            logger.error(f'Exception - {e}')
            
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            remove_member_from_db(member)
            await good_bye_message(self.bot,member)
        except Exception as e:
            logger.error(f'Exception - {e}',e)

    @commands.Cog.listener()
    async def on_guild_role_update(self,*args):
        before,after = args
        try:
            if not before.name == after.name:
                NewRoleChannelUtil.add_role_to_db(after)
        except Exception as e:
            logger.error(f'Exception - {e}',e)
async def setup(bot):
    await bot.add_cog(JoinParty(bot))


