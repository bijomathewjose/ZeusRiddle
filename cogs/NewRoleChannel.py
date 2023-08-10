import json
import discord
from discord.ext import commands
from settings import WELCOME_CHANNEL,WEBHOOK_ID,logging
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
            list=[discord.embeds.Embed.to_dict(embed) for embed in message.embeds]
            role_name,channel_name=list[0]['fields'][0]['value'],list[0]['fields'][1]['value']
            
            guild = message.guild
            is_guild,is_role =self.checkChannel(channel_name,guild),self.checkRole(role_name,guild)
            if  not is_role and not is_guild:
                permissions = discord.Permissions(add_reactions=False,manage_messages=True,manage_nicknames=True,speak=False)
                new_role = await guild.create_role(name=role_name,permissions=permissions)
                new_channel = await guild.create_text_channel(name=channel_name,category=guild.categories[0],)
                await new_channel.send(f"Role '{new_role.name}' and Channel '{new_channel.name}' created by {self.bot.user.mention}!")  
            else:
                channel = self.bot.get_channel(WELCOME_CHANNEL)
                if channel==message.channel:
                    logger.info(f'Role {role_name}' +' already exists ' if is_role else 'is created')
                    logger.info(f'Channel {channel_name}'+ ' already exists ' if not is_guild else ' is created')
                    await channel.send(f'{message.author.mention}  {f"Role `{role_name}` or Channel `{channel_name}` already exists" if is_role or not is_guild else ""}')
        except Exception as e:
            logger.error(f'Exception - {e}',e)


    def checkRole(self,role_name,guild):
        try:
            existing_roles = guild.roles
            role_exists = any(role.name == role_name for role in existing_roles)
            if role_exists:
                    return True
            return False
        except Exception as  e:
                logger.error(f'Exception - {e}',e)
                
    def checkChannel(self,channel_name,guild):
        try:
            existing_channels = guild.channels
            channel_exists = any(channel.name == channel_name for channel in existing_channels)
            if channel_exists:
                    return True
            return False
        except Exception as  e:
            logger.error(f'Exception - {e}',e)

async def setup(bot):
    await bot.add_cog(NewRoleChannel(bot))