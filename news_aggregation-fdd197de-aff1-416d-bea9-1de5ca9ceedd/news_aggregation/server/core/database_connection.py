import mysql.connector as sql

def get_db_connection():
    return sql.connect(
        host="localhost",
        user="root",
        passwd="Vicky@111222",
        database="news_db"
    )
