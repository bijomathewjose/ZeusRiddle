import logging
import discord
import mysql
from settings import WELCOME_CHANNEL
from settings import cursor,commit,mydb

logger=logging.getLogger("bot")
def get_fields_from_embed(message):
    try:
        field_list=[]
        for embed in message.embeds:
            field_list.append({field.name:field.value for field in embed.fields})
    except Exception as e:
        logger.error(f'Exception - {e}',e)
    return field_list

def checkChannel(channel_name,guild):
        try:
            existing_channels = guild.channels
            channel_exists = any(channel.name == channel_name for channel in existing_channels)
            if channel_exists:
                    return True
            return False
        except Exception as  e:
            logger.error(f'Exception - {e}',e)

async def add_new_role(*args,**kwargs):
    try:
        guild,role=args
        permissions = discord.Permissions(**kwargs)
        new_role= await guild.create_role(name=role,permissions=permissions)
        if new_role:
            add_role_to_db(new_role)
            return new_role
    except Exception as  e:
            logger.error(f'Exception - {e}',e)

def add_role_to_db(role:discord.Role):
    id,name=role.id,role.name
    try:
        sql=f'SELECT * FROM role where id = "{id}"'
        cursor.execute(sql)
        roles=cursor.fetchall()
        if roles:
            sql=f"UPDATE role SET name='{name}' WHERE id='{id}'"
        else:
            sql=f"INSERT INTO role (id,name) VALUES ('{id}','{name}')"
        cursor.execute(sql)
        commit()
    except mysql.connector.Error as e:
        mydb.rollback()
        logger.error(f'Database Error : {e}') 

async def send_result(**kwargs):
    embed ,channel= None,None
    if kwargs['new_channel'] and kwargs['new_role']:
        embed = discord.Embed(title="Success")
        embed.add_field(name='Role', value=f"{kwargs['new_role']} created",inline=False)
        embed.add_field(name='Channel', value=f"{kwargs['new_channel']} created",inline=False)
        channel = kwargs['new_channel']
    else:
        channel = kwargs['bot'].get_channel(WELCOME_CHANNEL)
        if channel == kwargs['message'].channel:
            embed = discord.Embed(title="Error")
            embed.add_field(name='Role', value=f"{kwargs['role_name']} already exists",inline=False)
            embed.add_field(name='Channel', value=f"{kwargs['channel_name']} already exists",inline=False)
    await channel.send(content=f'{kwargs["message"].author.mention}', embeds=[embed],)


def checkRole(role_name,guild):
        try:
            existing_roles = guild.roles
            role_exists = any(role.name == role_name for role in existing_roles)
            if role_exists:
                    return True
            return False
        except Exception as  e:
            logger.error(f'Exception - {e}',e)