import logging
import discord
from uuid import uuid4
from settings import cursor,commit,mydb
from settings import WELCOME_CHANNEL
from mysql.connector import Error
logger = logging.getLogger("bot")
def check_user_in_db(member):
    try:        
        sql=f"""SELECT * FROM user where id={member.id}"""
        cursor.execute(sql)
        data=cursor.fetchall()
    except Error as e:
        mydb.rollback()
        logger.error(f'Database Error : {e}')
    return data

async def add_user(member):
    try:
        role_name='Mortal'
        user_in_db=check_user_in_db(member)
        role=discord.utils.get(member.guild.roles, name=role_name)
        if not user_in_db and role:
            add_user_to_db(member,role)
            await member.add_roles(role)
            logger.info(f'{member.id} {member.name} added to DB ,assigned role - {role.name}')
        else:
            logger.error('New User has no roles associated')
    except ExceptionGroup as e:
        logger.error(f'Exception - {e}')    
def add_user_to_db(member:str,role:str)->None:
    try:
        cursor.execute(f"INSERT INTO user (id,name) VALUES('{member.id}','{(member.name)}')")
        cursor.execute(f"""INSERT INTO user_role_link (id,user_id,role_id) VALUES('{uuid4()}','{member.id}','{role.id}')""")
        commit()
    except Error as e:
        mydb.rollback()
        logger.error(f'Database Error : {e}')

async def message_channel(bot,member,channel):
    channel = bot.get_channel(WELCOME_CHANNEL)
    if channel:
        await channel.send(f'{member.mention} Welcome to {member.guild.name}')

async def direct_message_user(member):
    await member.send(f'Welcome to {member.guild.name} ? Ask if you have any doubts')

async def good_bye_message(bot,member):
    channel = bot.get_channel(WELCOME_CHANNEL)
    if channel:
        await channel.send(f'Goodbye {member.mention}, we will miss you ')

def remove_member_from_db(member):
    data=check_user_in_db(member)
    if data:
        try:
            cursor.execute(f"DELETE FROM user_role_link where user_id='{member.id}'")
            cursor.execute(f" DELETE FROM user where id='{member.id}'")
            commit()
        except Error as e:
            mydb.rollback()
            logger.error(f'Database Error : {e}')
