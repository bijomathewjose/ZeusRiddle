import discord
import logging
import mysql
from discord import app_commands
from settings import cursor,commit,mydb

logger = logging.getLogger("bot")

from uuid import uuid4

async def setup(bot):
    @app_commands.command(name='sync')
    async def sync(interaction: discord.Interaction,string: str):
        try:
            guild=interaction.guild
            cursor.execute("SELECT * FROM user_role_link")
            db_members=[(int(member['user_id']),int(member['role_id'])) for member in cursor.fetchall()]
            queries=[]
            sql_statement=None

            if string == 'from-discord-to-db':
                queries=[(str(uuid4()),member.id,role.id) for member in guild.members for role in member.roles if not ((member.id,role.id) in db_members or role.name=='@everyone') ]
                sql_statement="INSERT INTO user_role_link (id, user_id, role_id) VALUES(%s, %s, %s)"

            elif string == 'from-db-to-discord':

                for db_user_role in db_members:
                    user_id,role_id=db_user_role
                    user = discord.utils.get(guild.members, id=user_id)
                    role = discord.utils.get(user.roles,id=role_id) if user else None
                    if not user or not role:
                        queries.append(db_user_role) 
                sql_statement="DELETE FROM user_role_link WHERE user_id=%s AND role_id=%s"

            if(len(queries)>0):
                try:
                    cursor.executemany(sql_statement, queries)
                    commit()
                except mysql.connector.Error as e:
                    mydb.rollback()
                    logger.error(f'Database Error : {e}')
            logger.info('Discord user synced to to Database')
            await interaction.response.send_message(f"Updated users in db for {guild.name}",ephemeral=True)
        except Exception as e:
            logger.error(f'Exception - {e}',e)
    bot.tree.add_command(sync)