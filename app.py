import sqlite3
from flask import Flask

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Database opened successfully")

    conn.execute('CREATE TABLE IF NOT EXIST owner_table(OwnerId INTEGER PRIMARY KEY AUTOINCREMENT, Firstname TEXT, Lastname TEXT,'
                 ' Username TEXT, age INTEGER, Email TEXT, Password TEXT )')
    print("Table created successfully")

    conn.execute('CREATE TABLE IF NOT EXIST owner_table()')

    conn.execute()
    conn.close()