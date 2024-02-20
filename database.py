import sqlite3
import os
from functools import wraps


def db_connect(func):
    """ Handles the connection and cursor creation. Passes the cursor to the caller function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(os.path.join(os.getcwd(), 'database.db'))
        cursor = conn.cursor()
        result = func(cursor, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return wrapper


@db_connect
def create_table(cursor):
    """Initializes the database with 2 tables and a 'reporting' view"""

    sql = ('''CREATE TABLE IF NOT EXISTS LOG (
                     LOG_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                     DATE TEXT DEFAULT (strftime('%Y-%m-%d', 'now', 'localtime')),
                     TIME TEXT DEFAULT (strftime('%H:%M:%S', 'now', 'localtime')),
                     STATUS TEXT
                     );''')
    cursor.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS LINK (
                    LINK_ID integer
                        constraint LINK_pk
                        primary key autoincrement,
                    LOG_ID  integer
                        constraint LINK_LOG_LOG_ID_fk
                        references LOG,
                    LINK    TEXT,
                    TITLE   TEXT
                    );"""
    cursor.execute(sql)

    sql = """create view if not exists LINK_LIST as
                    select LINK.TITLE, LINK.LINK, l.DATE, l.TIME
                    from LINK inner join LOG L on L.LOG_ID = LINK.LOG_ID"""
    cursor.execute(sql)


@db_connect
def insert_log(cursor, status: str) -> None:
    """
    Inserts a log record into the LOG table with date, time and status of the script run.
    :param cursor: Created by the @db_connect wrapper function
    :param status: The status text to insert into the database's LOG table
    :return: None
    """
    cursor.execute("""INSERT INTO LOG (STATUS) VALUES (?)""", (status,))


@db_connect
def insert_link(cursor, link: str, title: str) -> None:
    """
    Inserts a new record into the LINK table. Called when there is a new article on the news page
    :param cursor: Created by the @db_connect wrapper function
    :param link: The URL of the news to be inserted into the LINK field
    :param title: The title of the news to be inserted into the TITLE field
    :return:
    """
    log_id = cursor.execute("""SELECT MAX(LOG_ID) FROM LOG""").fetchall()[0][0]
    cursor.execute("""INSERT INTO LINK  (LOG_ID, LINK, TITLE) VALUES (?, ?, ?)""", (log_id, link, title, ))


@db_connect
def check_link(cursor, link: str):
    """
    Checks if the link param exists in the LINK column of the LINK table.
    :param cursor: Created by the @db_connect wrapper function
    :param link: The link of the article to be checked against the LINK column of the LINK table.
    :return:
    """
    cursor.execute('''SELECT EXISTS (SELECT 1 FROM LINK L WHERE LINK = (?))''', (link, ))
    result = cursor.fetchone()[0]
    return bool(result)


if __name__ == '__main__':
    # Teszt
    create_table()
    insert_log(status="Success")
    insert_link(link="https://telex.hu", title="TELEX")