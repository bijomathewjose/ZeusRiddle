import json
import discord
from discord.ext import commands
from settings import WELCOME_CHANNEL
class NewRoleChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author == self.bot.user:
            return
        try:
            if message.webhook_id==1137248549835382785:
                await self.handle_webhook_payload(message)
            channel = self.bot.get_channel(WELCOME_CHANNEL)
            if channel==message.channel:
                await channel.send(f'{message.author.mention} Welcome to {channel.name} channel')
        except Exception as e:
            print('exception:',e)
    
    async def handle_webhook_payload(self,message):
        try:
            list=[discord.embeds.Embed.to_dict(embed) for embed in message.embeds]
            role_name,channel_name=list[0]['fields'][0]['value'],list[0]['fields'][1]['value']
            
            guild = message.guild
        
            if  self.checkRole(role_name,guild) and self.checkChannel(channel_name,guild):
                permissions = discord.Permissions(add_reactions=False,manage_messages=True,manage_nicknames=True,speak=False)
                new_role = await guild.create_role(name=role_name,permissions=permissions)
                new_channel = await guild.create_text_channel(name=channel_name,category=guild.categories[0],)
                await message.channel.send(f"Role '{new_role.name}' and Channel '{new_channel.name}' created by {self.bot.user.mention}!")  
                print(f"Role '{new_role.name}' and Channel '{new_channel.name}' created !")
        except Exception as e:
            print(e) 

    def checkRole(self,role_name,guild):
        existing_roles = guild.roles
        role_exists = any(role.name == role_name for role in existing_roles)
        if role_exists:
                print(f"Role '{role_name}' already exists.So no further update")
                return False
        return True

    def checkChannel(self,channel_name,guild):
        existing_channels = guild.channels
        channel_exists = any(channel.name == channel_name for channel in existing_channels)
        if channel_exists:
                print(f"Channel '{channel_name}' already exists.")
                return False
        return True
    
async def setup(bot):
    await bot.add_cog(NewRoleChannel(bot))