import os

from discordwebhook import Discord
from dotenv import load_dotenv
from datetime import datetime


def post_message(message: str) -> None:
    """
    Posts a message into a Discord channel via webhook. URL of Discord room is loaded from .env
    :param message: string to be posted to the discord channel
    :return:
    """
    load_dotenv()
    message = '@everyone ' + message
    discord = Discord(url=os.getenv('DISCORD_WEBHOOK'))
    discord.post(content=message)


def post_log(message: str) -> None:
    """
    Posts a message into a Discord channel via webhook. URL of Discord room is loaded from .env
    :param message: string to be posted to the discord channel
    :return:
    """
    load_dotenv()
    discord = Discord(url=os.getenv('LOG_WEBHOOK'))
    message = message + ': ' + str(datetime.now())
    discord.post(content=message)

