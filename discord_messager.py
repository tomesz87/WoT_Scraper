import os

from discordwebhook import Discord
from dotenv import load_dotenv


def post_message(message: str) -> None:
    load_dotenv()

    discord = Discord(url=os.getenv('DISCORD_WEBHOOK'))
    discord.post(content=message)

