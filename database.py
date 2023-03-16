import sqlite3
from functools import wraps


def db_connect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        result = func(cursor, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return wrapper


@db_connect
def create_table(cursor):
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
def insert_log(cursor, status):
    cursor.execute("""INSERT INTO LOG (STATUS) VALUES (?)""", (status,))


@db_connect
def insert_link(cursor, link, title):
    log_id = cursor.execute("""SELECT MAX(LOG_ID) FROM LOG""").fetchall()[0][0]
    cursor.execute("""INSERT INTO LINK  (LOG_ID, LINK, TITLE) VALUES (?, ?, ?)""", (log_id, link, title, ))


if __name__ == '__main__':
    create_table()
    insert_log(status="Success")
    insert_link(link="https://telexasdasa.hu", title="TELEKasdasXsss")