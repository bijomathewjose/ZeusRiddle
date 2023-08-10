import discord
from discord import app_commands
from settings import cursor,commit,logging
logger = logging.getLogger("bot")
from uuid import uuid4
class Sync(app_commands.Group):
    @app_commands.command(name="discord-to-db")
    async def sync(self,interaction: discord.Interaction):
        try:
            guild=interaction.guild
            self.sync_to_db(guild)
            logger.info('Discord user synced to to Database')
            await interaction.response.send_message(f"Updated users in db for {guild.name}",ephemeral=True)
        except Exception as e:
            logger.error(f'Exception - {e}',e)
    @app_commands.command(name="db-to-discord")
    async def db_to_discord(self,interaction: discord.Interaction):
        try:
            guild=interaction.guild
            sql=f"""SELECT * FROM user_role_link"""
            cursor.execute(sql)
            db_user_role_links=cursor.fetchall()
            users=guild.members
            for db_user_role in db_user_role_links:
                for user in users:
                    if db_user_role['user_id']==str(user.id):
                        if not any(db_user_role['role_id']==str(role.id) for role in user.roles):
                            role=discord.utils.get(guild.roles,id=int(db_user_role['role_id']))
                            await user.add_roles(role)
            await interaction.response.send_message(f"Updated roles in db for {guild.name}",ephemeral=True)
            pass
        except Exception as e:
            logger.error(f'Exception - {e}',e)
    @app_commands.command(name="roles-to-db")
    async def roles_to_db(self,interaction: discord.Interaction):
        try:
            guild=interaction.guild
            await self.sync_to_db_roles(guild)
            await interaction.response.send_message(f"Updated roles in roles for {guild.name}",ephemeral=True)
            pass
        except Exception as e:
            logger.error(f'Exception - {e}',e)

    async def sync_to_db_roles(self,guild):
        try:
            sql=f"""SELECT * FROM role"""
            cursor.execute(sql)
            db_roles=cursor.fetchall()
            for role in guild.roles:
                values=f"""'{role.id}','{role.name}'"""
                sql=f"""INSERT INTO role (id,name) VALUES({values})"""
                if not any(str(role.id) == db_role['id'] for db_role in db_roles):
                    cursor.execute(sql) 
                    commit()
        except Exception as  e:
            logger.error(f'Exception - {e}',e)
    def check_user(self,db_members,member,role):
        try:
            return any(db_member['user_id']==str(member.id) and db_member['role']==role.name for db_member in db_members)
        except Exception as  e:
            logger.error(f'Exception - {e}',e)
    def sync_to_db(self,guild):
        try:
            sql=f"""SELECT * FROM user"""
            cursor.execute(sql)
            db_members=cursor.fetchall()
            for member in guild.members:
                for role in member.roles: 
                    values=f"""'{uuid4()}','{member.id}','{role.id}''"""
                    sql=f"""INSERT INTO user (id,user_id,role,id) VALUES({values})"""
                    if not (self.check_user(db_members,member,role) or role.name=='@everyone'):
                        cursor.execute(sql) 
                        commit()
        except Exception as  e:
            logger.error(f'Exception - {e}',e)
async def setup(bot):
    bot.tree.add_command(Sync(name='sync'))