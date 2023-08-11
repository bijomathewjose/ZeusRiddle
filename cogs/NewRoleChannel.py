import discord
import logging
from discord.ext import commands
from settings import WELCOME_CHANNEL,WEBHOOK_ID
from utils import NewRoleChannelUtil

logger = logging.getLogger("bot")

class NewRoleChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author == self.bot.user:
            return
        try:
            if message.webhook_id==WEBHOOK_ID:
                await self.handle_webhook_payload(message)
        except Exception as e:
            logger.error(f'Exception - {e}',e)
    
    async def handle_webhook_payload(self,message):
        try:
            role_name,channel_name=NewRoleChannelUtil.get_fields_from_embed(message)[0].values()
            guild = message.guild
            new_channel,new_role =None,None
            is_guild,is_role =NewRoleChannelUtil.checkChannel(channel_name,guild),NewRoleChannelUtil.checkRole(role_name,guild)
            if  not is_role and not is_guild:
                new_role=await NewRoleChannelUtil.add_new_role(guild,role_name,add_reactions=False,manage_messages=True,manage_nicknames=True,speak=False)
                new_channel = await guild.create_text_channel(name=channel_name,category=guild.categories[0])
            await NewRoleChannelUtil.send_result(role_name=role_name,channel_name=channel_name,new_channel=new_channel,new_role=new_role,message=message,bot=self.bot)
        except Exception as e:
            logger.error(f'Exception - {e}',e)

    
                

async def setup(bot):
    await bot.add_cog(NewRoleChannel(bot))