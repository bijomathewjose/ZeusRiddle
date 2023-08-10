import discord
from discord import app_commands
from settings import cursor,commit,logging
logger = logging.getLogger("bot")
from uuid import uuid4
async def setup(bot):
    @app_commands.command(name="sync")
    async def sync(interaction: discord.Interaction):
        try:
            guild=interaction.guild
            sql=f"""SELECT * FROM user"""
            cursor.execute(sql)
            db_members=cursor.fetchall()
            sync_to_db(guild,db_members)
            logger.info('Discord user synced to to Database')
            await interaction.response.send_message(f"Updated users in db for {guild.name}",ephemeral=True)
        except Exception as e:
            logger.error(f'Exception - {e}',e)
    bot.tree.add_command(sync)

    def check_user(db_members,member,role):
        try:
            return any(db_member['user_id']==str(member.id) and db_member['role']==role.name for db_member in db_members)
        except Exception as  e:
            logger.error(f'Exception - {e}',e)
             
    def sync_to_db(guild,db_members):
        try:
            for member in guild.members:
                for role in member.roles: 
                    values=f"""'{member.id}','{member.name}','{role.name}','{uuid4()}'"""
                    sql=f"""INSERT INTO user (user_id,name,role,id) VALUES({values})"""
                    if not (check_user(db_members,member,role) or role.name=='@everyone'):
                        cursor.execute(sql) 
                        commit()
        except Exception as  e:
            logger.error(f'Exception - {e}',e)