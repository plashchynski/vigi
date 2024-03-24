"""
This file contains the Database class which is used to interact with the SQLite database
"""

import logging
import sqlite3

class Database:
    """
    The Database class is used to interact with the SQLite database
    """
    def __init__(self, db_path):
        """
        Initialize the database connection
        db_path: str, the path to the database file
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = self.dict_row_factory

    def dict_row_factory(self, cursor, row):
        """
        Convert the row to a dictionary
        cursor: sqlite3.Cursor
        row: sqlite3.Row

        The idea was taken from: https://stackoverflow.com/a/3300514
        """

        result = {}

        for idx, col in enumerate(cursor.description):
            result[col[0]] = row[idx]

        return result

    def init_db(self):
        """
        Initialize the database with the necessary tables and indexes
        create the database file if it does not exist
        create the table if it does not exist
        """
        logging.info("Initializing database at %s", self.db_path)
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS recordings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            camera_id INTEGER NOT NULL,
            tags TEXT
        );
        """
        self.conn.execute(create_table_sql)

        add_index_sql = """
        CREATE INDEX IF NOT EXISTS idx_recordings ON recordings (date, time, camera_id);
        """
        self.conn.execute(add_index_sql)
        logging.info("Database initialized")

    def add_recording(self, date, time, camera_id, tags):
        """
        Add a recording to the database
        """
        logging.debug("Adding recording to database: %s %s %s %s",
                      date, time, camera_id, tags)
        self.conn.execute("INSERT INTO recordings (date, time, camera_id, tags) VALUES (?, ?, ?, ?)",
                          (date, time, camera_id, tags))
        self.conn.commit()

    def find_recording(self, date, time, camera_id):
        """
        Find the recordings for the given date
        date: str, the date in the format YYYY-MM-DD
        time: str, the time in the format HH:MM:SS
        camera_id: int, the id of the camera
        """
        logging.debug("Finding recording in database: %s, %s, %s",
                      date, time, camera_id)
        cursor = self.conn.execute("SELECT * FROM recordings WHERE date = ? AND time = ? AND camera_id = ?",
                                   [date, time, camera_id])
        return cursor.fetchone()

    def delete_recording(self, date, time, camera_id):
        """
        Delete the recording for the given date, time and camera_id
        date: str, the date in the format YYYY-MM-DD
        time: str, the time in the format HH:MM:SS
        camera_id: int, the id of the camera
        """
        logging.debug("Deleting recording from database: %s, %s, %s",
                      date, time, camera_id)
        self.conn.execute("DELETE FROM recordings WHERE date = ? AND time = ? AND camera_id = ?",
                          [date, time, camera_id])
        self.conn.commit()

    def close(self):
        """
        Close the database connection
        """
        logging.info("Closing database connection")
        self.conn.close()
        self.conn = None

    def integrity_check(self):
        """
        Run the integrity check on the database
        """
        logging.info("Running integrity check on the database")
        self.conn.execute("PRAGMA integrity_check")
        logging.info("Integrity check completed")
