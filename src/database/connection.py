import sqlite3


class ConnectionDb:

    connection = sqlite3.connect("database/syncora.db")
    cursor = connection.cursor()

    def get_cursor(self):
        return self.cursor

    def create_tables(self):
        cursor = self.get_cursor()
        cursor.executescript(
            """CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                image TEXT,
                runtime TEXT,
                dependencies TEXT,
                commands TEXT,
                ports TEXT,
                env TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                services TEXT NOT NULL, -- JSON array of service names
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        self.connection.commit()
