import logging
import sqlite3

class Database:
    def __init__(self, db_path):
        """
        Initialize the database connection
        db_path: str, the path to the database file
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)

    def init_db(self):
        """
        Initialize the database with the necessary tables and indexes
        create the database file if it does not exist
        create the table if it does not exist
        """
        logging.info(f"Initalizing database at {self.db_path}")
        self.create_table_sql = """
        CREATE TABLE IF NOT EXISTS recordings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            camera_id INTEGER NOT NULL,
            tags TEXT
        );
        """
        self.conn.execute(self.create_table_sql)

        self.add_index = """
        CREATE INDEX IF NOT EXISTS idx_recordings ON recordings (date, time, camera_id);
        """
        self.conn.execute(self.add_index)
        logging.info("Database initialized")

    def add_recording(self, date, time, camera_id, tags):
        logging.debug(f"Adding recording to database: {date} {time} {camera_id} {tags}")
        self.conn.execute("INSERT INTO recordings (date, time, camera_id, tags) VALUES (?, ?, ?, ?)", (date, time, camera_id, tags))
        self.conn.commit()

    def close(self):
        logging.info("Closing database connection")
        self.conn.close()
        self.conn = None
