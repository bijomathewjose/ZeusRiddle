from uuid import uuid4
import discord
from discord.ext import commands
from settings import WELCOME_CHANNEL,cursor,commit,logging
logger = logging.getLogger("bot")
class JoinParty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            role_name='Mortal'
            sql=f"""SELECT * FROM user where user_id={member.id} """
            cursor.execute(sql)
            data=cursor.fetchall()
            if not data:
                sql=f"""INSERT INTO user (user_id,name,role,id) VALUES('{member.id}','{(member.name)}','{role_name}','{uuid4()}')"""
                cursor.execute(sql)
                commit()
            role = discord.utils.get(member.guild.roles, name=role_name)
            if role is not None:
                await member.add_roles(role)
            else:
                print('role is none ,user has no roles associated')
            channel = self.bot.get_channel(WELCOME_CHANNEL)
            if channel:
                logger.info(f'{member.id} {member.name} joined guild',member)
                await channel.send(f'{member.mention} Welcome to {member.guild.name}')
            await member.send(f'Welcome to {member.guild.name} ? Ask if you have any doubts')
        except Exception as e:
            logger.error(f'Exception - {e}',e)
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            sql=f"""DELETE FROM user where user_id='{member.id}'"""
            cursor.execute(sql)
            commit()
            channel = self.bot.get_channel(WELCOME_CHANNEL)
            if channel:
                await channel.send(f'{member.mention} Goodbye')
        except Exception as e:
            logger.error(f'Exception - {e}',e)
    
async def setup(bot):
    await bot.add_cog(JoinParty(bot))


