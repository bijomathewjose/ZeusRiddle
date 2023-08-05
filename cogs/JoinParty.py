import json
import discord
from discord.ext import commands
from settings import WELCOME_CHANNEL
class JoinParty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            channel = self.bot.get_channel(WELCOME_CHANNEL)
            if channel:
                await channel.send(f'{member.mention} Welcome to {member.guild.name}')
            await member.send(f'Welcome to {member.guild.name} ? Ask if you have any doubts')
        except Exception as e:
            print(e)
    @commands.Cog.listener()   
    async def on_message(self, message:discord.Message):
        if message.author == self.bot.user:
            return
        try:
            if message.webhook_id:
                await self.handle_webhook_payload(message)
            channel = self.bot.get_channel(WELCOME_CHANNEL)
            if channel==message.channel:
                await channel.send(f'{message.author.mention} Welcome to {channel.name} channel')
        except Exception as e:
            print('exception:',e)
    
    async def handle_webhook_payload(self,message):
        try:
            obj = json.loads(message.content.replace("'", '"'))
            role_name = obj['role']
            channel_name = obj['channel'].lower().replace(' ', '-')
            
            guild = message.guild
            existing_roles = guild.roles
            existing_channels = guild.channels
            
            role_exists = any(role.name == role_name for role in existing_roles)
            channel_exists = any(channel.name == channel_name for channel in existing_channels)

            if role_exists:
                print(f"Role '{role_name}' already exists.")
            if channel_exists:
                print(f"Channel '{channel_name}' already exists.")
            if not (role_exists and channel_exists):
                new_role = await guild.create_role(name=role_name)
                new_channel = await guild.create_text_channel(name=channel_name)
                await message.channel.send(f"Role '{new_role.name}' and Channel '{new_channel.name}' created!")   
        except Exception as e:
            print(e) 
    
async def setup(bot):
    await bot.add_cog(JoinParty(bot))


