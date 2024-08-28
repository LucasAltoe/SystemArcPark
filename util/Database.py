import sqlite3

class Database:
    @classmethod
    def createConnection(cls): # Use "cls" instead of self (used in instance method) in the first parameter of classmethod.
        conn = sqlite3.connect("data.db")
        return conn