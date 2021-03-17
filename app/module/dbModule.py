import sqlite3

class DB():
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()