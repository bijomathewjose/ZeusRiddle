import discord
import logging
import mysql
from discord import app_commands
from settings import cursor,commit,mydb
from utils import SyncUtil
logger = logging.getLogger("bot")

from uuid import uuid4
class Sync(app_commands.Group):
    @app_commands.command(name="from-discord-to-db",description='Update user roles in database from discord')
    async def sync(self,interaction: discord.Interaction):
        try:
            cursor.execute("SELECT * FROM user_role_link")
            db_members=[(int(member['user_id']),int(member['role_id'])) for member in cursor.fetchall()]
            queries=[(str(uuid4()),member.id,role.id) for member in interaction.guild.members for role in member.roles if not ((member.id,role.id) in db_members or role.name=='@everyone') ]
            if(len(queries)>0):
                try:
                    cursor.executemany("INSERT INTO user_role_link (id, user_id, role_id) VALUES(%s, %s, %s)", queries)
                    commit()
                except mysql.connector.Error as e:
                    mydb.rollback()
                    logger.error(f'Database Error : {e}')
            logger.info('Discord user synced to to Database')
            await interaction.response.send_message(f"Updated users in db for {interaction.guild.name}",ephemeral=True)
        except Exception as e:
            logger.error(f'Exception - {e}',e)

    @app_commands.command(name="from-db-to-discord",description='Update user roles in discord from database')
    async def db_to_discord(self,interaction: discord.Interaction):
        try:
            guild=interaction.guild
            cursor.execute('SELECT * FROM user_role_link')
            db_user_role_links= cursor.fetchall()
            queries=[]
            for db_user_role in db_user_role_links:
                user_id,role_id=int(db_user_role['user_id']),int(db_user_role['role_id'])
                user = discord.utils.get(guild.members, id=user_id)
                role = discord.utils.get(user.roles,id=role_id) if user else None
                if not user:
                    queries.append((user_id,)) 
                elif not role: 
                    await user.add_roles(discord.utils.get(guild.roles,id=role_id))
            if(len(queries)>0):
                try:
                    sql_statement="DELETE FROM user_role_link WHERE user_id=%s"
                    cursor.executemany(sql_statement,queries)
                    commit()
                except mysql.connector.Error as e:
                    mydb.rollback()
                    logger.error(f'Database Error : {e}')
            await interaction.response.send_message(f"Updated roles in db for {guild.name}",ephemeral=True)
        except Exception as e:
            logger.error(f'Exception - {e}',e)


    @app_commands.command(name="roles-to-db",description='Update roles in database from discord')
    async def roles_to_db(self,interaction: discord.Interaction):
        try:
            guild=interaction.guild
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
            await interaction.response.send_message(f"Updated roles in roles for {guild.name}",ephemeral=True)
        except Exception as e:
            logger.error(f'Exception - {e}',e)

async def setup(bot):
    bot.tree.add_command(Sync(name='sync'))