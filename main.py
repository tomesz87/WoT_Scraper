import os

from discord_messager import post_message, post_log
from scraper import get_links
from database import check_link, create_table, insert_link, insert_log
from dotenv import load_dotenv


load_dotenv()

DEBUG = bool(os.getenv('DEBUG'))

post_log("Start") if DEBUG else None
create_table()
post_log("'create_table' done") if DEBUG else None

try:
    insert_log(status="Successful")
    for url, title in get_links():
        if not check_link(url):
            insert_link(link=url, title=title)
            post_log("New link inserted to DB") if DEBUG else None
            post_message(url)
            post_log("Posted to Discord") if DEBUG else None
    post_log("Done") if DEBUG else None

except TypeError as e:
    insert_log(status=e.args)
