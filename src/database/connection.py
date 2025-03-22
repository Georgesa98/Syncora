import sqlite3
import os


class ConnectionDb:
    """Handles SQLite database connection and initialization."""

    _instance = None

    def __new__(cls):
        """Singleton pattern to ensure only one instance of the class is created."""
        if cls._instance is None:
            cls._instance = super(ConnectionDb, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize database path and connection."""
        self.db_path = self._get_db_path()
        self.connection = self._get_db_connection()
        self.initialize_database()

    def _get_db_path(self):
        """Returns the hidden database path based on the OS."""
        db_dir = (
            os.path.join(os.getenv("LOCALAPPDATA"), "syncora")
            if os.name == "nt"
            else os.path.expanduser("~/.syncora")
        )
        os.makedirs(db_dir, exist_ok=True)
        return os.path.join(db_dir, "syncora.db")

    def _get_db_connection(self):
        """Creates and returns a SQLite database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize_database(self):
        """Creates required tables if they don't exist."""
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.executescript(
                """
                CREATE TABLE IF NOT EXISTS services (
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

    def execute_query(self, query, params=None):
        """Executes a query and returns the result."""
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def close_connection(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
