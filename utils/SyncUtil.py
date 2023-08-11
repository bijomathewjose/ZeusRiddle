import logging
import discord
import mysql
from uuid import uuid4
from settings import cursor,commit,mydb


logger = logging.getLogger("bot")

def sync_to_db(guild):
    try:
        db_members=get_db_user_list('user_role_link')
        run_queries(guild.members,db_members)
    except mysql.connector.Error as  e:
        logger.error(f'Exception - {e}',e)

def check_user(db_members,member,role):
    try:
        return any(db_member['user_id']==str(member.id) and db_member['role_id']==str(role.id) for db_member in db_members)
    except Exception as  e:
        logger.error(f'Exception - {e}',e)

def get_db_user_list(item):
    sql=f"""SELECT * FROM {item}"""
    cursor.execute(sql)
    return cursor.fetchall()

def run_queries(members:discord.Guild.members,db_members):
    queries=[]
    for member in members:
        for role in member.roles:  
            if not (check_user(db_members,member,role) or role.name=='@everyone'):
                queries.append( (str(uuid4()), str(member.id), str(role.id)))    
    if(len(queries)>0):
        try:
            cursor.executemany("INSERT INTO user_role_link (id, user_id, role_id) VALUES(%s, %s, %s)", queries)
            commit()
        except mysql.connector.Error as e:
            mydb.rollback()
            logger.error(f'Database Error : {e}')

async def sync_to_guild(guild):
    db_user_role_links=get_db_user_list('user_role_link')
    users=guild.members
    queries=[]
    for db_user_role in db_user_role_links:
        user_in_discord=False
        for user in users:
            if db_user_role['user_id']==str(user.id):
                user_in_discord=True
                if not any(db_user_role['role_id']==str(role.id) for role in user.roles):
                    role=discord.utils.get(guild.roles,id=int(db_user_role['role_id']))
                    await user.add_roles(role)
        if not user_in_discord:
            queries.append((db_user_role['user_id'],))
    if(len(queries)>0):
        try:
            sql_statement="DELETE FROM user_role_link WHERE user_id=%s"
            cursor.executemany(sql_statement,queries)
            commit()
        except mysql.connector.Error as e:
            mydb.rollback()
            logger.error(f'Database Error : {e}')

async def sync_to_db_roles(self,guild):
    try:
        try:
            db_roles=get_db_user_list('role')
        except mysql.connector.Error as e:
            logger.error(f'Exception - {e}')
        queries=[]
        for role in guild.roles:            
            if not any(str(role.id) == db_role['id'] for db_role in db_roles):
                queries.append((role.id,role.name))
        try:
            cursor.executemany("INSERT INTO role (id,name) VALUES( %s,%s)", queries)
            commit()
        except mysql.connector.Error as e:
            mydb.rollback()
            logger.error(f'Database Error : {e}')
    except Exception as  e:
        logger.error(f'Exception - {e}')