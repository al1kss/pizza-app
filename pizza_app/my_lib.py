import sqlite3
import os
from pathlib import Path

class DatabaseManager:
    def __init__(self, name: str):
        db_path = Path(__file__).parent / "assets"/ "databases" / name
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def search(self, query):
        result = self.cursor.execute(query).fetchall()
        return result

    def close(self):
        self.connection.close()

    def run_save(self, query):
        self.cursor.execute(query)
        self.connection.commit()