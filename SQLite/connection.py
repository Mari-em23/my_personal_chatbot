import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

def get_connection(): # fresh connection when needed
    return sqlite3.connect(DATABASE)

def get_database_path():
    return DATABASE
