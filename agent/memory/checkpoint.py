import sqlite3
import os
from langgraph.checkpoint.sqlite import SqliteSaver

def get_db_url():
    current_path = os.path.dirname(__file__)
    BASE_DIR = os.path.dirname(os.path.dirname(current_path))
    DB_DIR = os.path.join(BASE_DIR, "db", "sqlite")
    db_url = os.path.join(DB_DIR, "checkpoint.db")
    return db_url

def get_checkpoint():
    db_url = get_db_url()
    checkpointer = SqliteSaver(sqlite3.connect(db_url, check_same_thread=False))
    checkpointer.setup()
    return checkpointer