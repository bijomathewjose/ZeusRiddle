import os
import discord
import mysql.connector
from dotenv import load_dotenv
import logging
from logging.config import dictConfig

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID=int(os.getenv('GUILD_ID'))
GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))
WELCOME_CHANNEL=int(os.getenv('GENERAL'))
DB_PASS=os.getenv('DB_PASS')
WEBHOOK_ID=int(os.getenv('WEBHOOK_ID'))
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=DB_PASS,
        database="zeus"
    )
cursor = mydb.cursor(dictionary=True)
commit = mydb.commit

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {"format": "%(levelname)-10s - %(name)-15s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "bot": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)