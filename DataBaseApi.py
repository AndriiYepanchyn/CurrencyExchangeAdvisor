import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor


class DataBaseApi:
    
    db_querries = {
        "banks" : """CREATE TABLE IF NOT EXISTS banks (
            bank_id TEXT PRIMARY KEY NOT NULL,
            bank_name TEXT NOT NULL,
            bank_url TEXT NOT NULL
            );""",
        "currency" : """CREATE TABLE IF NOT EXISTS currency (
            currency_id TEXT PRIMARY KEY NOT NULL,
            currency_name TEXT NOT NULL
            );""",
        "statistics" : """CREATE TABLE IF NOT EXISTS statistics (
            record_id TEXT PRIMARY KEY NOT NULL,
            date DATE,
            bank_id TEXT NOT NULL,
            currency_id TEXT NOT NULL,
            value REAL NOT NULL
            );""",
        "suffixes" : """CREATE TABLE IF NOT EXISTS suffixes (
            suffixes_id TEXT PRIMARY KEY NOT NULL,
            bank_id TEXT NOT NULL,
            suffix TEXT NOT NULL,
            expected_response_format TEXT
            );""",
        "banks_info": """CREATE VIEW IF NOT EXISTS BANKS_INFO AS 
            SELECT 
                 bank_id AS "Bank id",
                 bank_name AS "Bank name",
                 bank_url AS "Bank's web page",
                 suffix AS "Suffix",
                 expected_response_format AS "Expected response format"
            FROM banks
            JOIN suffixes USING(bank_id); """,     
        "settings" : ""
    }
    
    def __init__(self, db_type="sqlite", config=None):
        """
        db_type: "sqlite" або "postgres"
        config: dict із параметрами підключення
        """
        self.db_type = db_type
        self.config = config or {}
        self.conn = None

    def connect(self):
        if self.db_type == "sqlite":
            base_dir = os.path.dirname(__file__)
            db_dir = os.path.join(base_dir, "database")
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "app.db")
            
            self.conn = sqlite3.connect(db_path)
            
        elif self.db_type == "postgres":
            self.conn = psycopg2.connect(
                dbname=self.config.get("dbname", "appdb"),
                user=self.config.get("user", "postgres"),
                password=self.config.get("password", "postgres"),
                host=self.config.get("host", "localhost"),
                port=self.config.get("port", 5432),
                cursor_factory=RealDictCursor
            )
        else:
            raise ValueError("Невідомий тип бази даних")

    def create_tables(self, db_requests : dict):
        cursor = self.conn.cursor()
        
        for querry in db_requests.values():
            cursor.execute(querry)

        self.conn.commit()

    def execute(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params or ())
        self.conn.commit()
        return cursor

    def fetchall(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall()
    
    def get_table(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params or [])

        headers = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        return headers, rows

    def close(self):
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # приклад із SQLite
    db = DataBaseApi("sqlite")
    db.connect()
    db.create_tables(DataBaseApi.db_querries)
    db.close()

    # приклад із PostgreSQL
    # pg_conf = {"dbname": "mydb", "user": "postgres", "password": "1234", "host": "localhost"}
    # db = DatabaseAPI("postgres", pg_conf)
    # db.connect()
    # db.create_tables()
    # db.close()
