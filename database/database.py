import sqlite3
from pathlib import Path


DATABASE_PATH = "database/hr.db"


def get_connection():
    """
    Create and return a SQLite database connection.
    """

    Path("database").mkdir(
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """
    Create all HR database tables if they don't exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    # -----------------------------------------------------
    # Employees
    # -----------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT,
            designation TEXT,
            join_date TEXT,
            manager_id TEXT,
            password_hash TEXT NOT NULL,
            is_active INTEGER DEFAULT 1
        )
        """
    )

    # -----------------------------------------------------
    # Leave Balances
    # -----------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS leave_balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            leave_type TEXT NOT NULL,
            allocated REAL DEFAULT 0,
            used REAL DEFAULT 0,
            remaining REAL DEFAULT 0,

            FOREIGN KEY(employee_id)
                REFERENCES employees(employee_id)
        )
        """
    )

    # -----------------------------------------------------
    # Leave History
    # -----------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS leave_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            leave_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            days REAL NOT NULL,
            status TEXT NOT NULL,
            reason TEXT,

            FOREIGN KEY(employee_id)
                REFERENCES employees(employee_id)
        )
        """
    )

    # -----------------------------------------------------
    # Holidays
    # -----------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            holiday_date TEXT NOT NULL,
            holiday_name TEXT NOT NULL
        )
        """
    )

    connection.commit()

    connection.close()