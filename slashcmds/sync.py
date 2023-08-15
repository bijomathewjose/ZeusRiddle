import discord
import logging
import mysql
from discord import app_commands
from settings import cursor,commit,rollback

logger = logging.getLogger("bot")

from uuid import uuid4

async def setup(bot):
    @app_commands.command(name='sync')
    async def sync(interaction: discord.Interaction,string: str):
        try:
            guild=interaction.guild
            cursor.execute("SELECT * FROM user_role_link")
            db_members=[(int(member['user_id']),int(member['role_id'])) for member in cursor.fetchall()]
            discord_members=[(member.id,role.id) for member in guild.members for role in member.roles if not role.name=='@everyone']
            insert_queries,delete_queries=None,None

            if string == 'discord-to-db':
                insert_queries=[(str(uuid4()),member[0],member[1])for member in discord_members if not member in db_members]
                delete_queries=[(member[0],member[1]) for member in db_members if not member in discord_members]
                
            elif string == 'db-to-discord':
                for db_user_role in db_members:
                    user_id,role_id=db_user_role
                    user = discord.utils.get(guild.members, id=user_id)
                    role = discord.utils.get(user.roles,id=role_id) if user else None
                    if user and role:
                        user.add_roles(role)                        
                    elif user and role==None:
                        user.remove_roles(role)
            
            if insert_queries or delete_queries:        
                try:
                    if insert_queries:
                        cursor.executemany("INSERT INTO user_role_link (id, user_id, role_id) VALUES(%s, %s, %s)", insert_queries)
                    if delete_queries:
                        cursor.executemany("DELETE FROM user_role_link WHERE user_id=%s AND role_id=%s", delete_queries)
                    
                        commit()
                except mysql.connector.Error as e:
                    rollback()
                    logger.error(f'Database Error : {e}')

            logger.info('Discord user synced to to Database')

            if string == 'discord-to-db':
                await interaction.response.send_message(f"Synced discord to database for {guild.name}",ephemeral=True)
            elif string == 'db-to-discord':
                await interaction.response.send_message(f"Synced database to discord for {guild.name}",ephemeral=True)
            else:
                embed=discord.Embed(title=f"sync commands ",description=f"Synced commands",color=0x00ff00)
                embed.add_field(name='command 1',value='discord-to-db',inline=False)
                embed.add_field(name='command 2',value='db-to-discord',inline=False)
                await interaction.response.send_message(f"Invalid Command,Check the list below",embeds=[embed])
        except Exception as e:
            logger.error(f'Exception - {e}',e)
    bot.tree.add_command(sync)