from database.database import (
    get_connection,
    initialize_database
)

from services.auth_service import (
    hash_password
)


def seed_employees():

    connection = get_connection()

    cursor = connection.cursor()

    employees = [
        (
            "I20101",
            "Rajarajan Ramanathan",
            "rajarajan.ramanathan@ideas2it.com",
            "Engineering",
            "Tech Architect",
            "2020-11-05",
            "EMP2001",
            hash_password("test@123"),
            1
        ),
        (
            "I20102",
            "Senthilkumar D",
            "senthilkumar@ideas2it.com",
            "Engineering",
            "Tech Architect",
            "2020-11-05",
            "EMP2001",
            hash_password("test@123"),
            1
        ),
        (
            "I16003",
            "Nijanthan D",
            "kumar@company.com",
            "Engineering",
            "Software Engineer",
            "2024-01-15",
            "EMP2001",
            hash_password("test@123"),
            1
        ),
        (
            "I20203",
            "Saravanakumar",
            "sarvanakumar@company.com",
            "HR",
            "HR Executive",
            "2021-08-02",
            "EMP4001",
            hash_password("test@123"),
            1
        )
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO employees
        (
            employee_id,
            name,
            email,
            department,
            designation,
            join_date,
            manager_id,
            password_hash,
            is_active
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        employees
    )

    connection.commit()

    connection.close()


def seed_leave_balances():

    connection = get_connection()

    cursor = connection.cursor()

    balances = [

        # I20101
        (
            "I20101",
            "Casual Leave",
            12,
            7,
            5
        ),
        (
            "I20101",
            "Sick Leave",
            12,
            4,
            8
        ),
        (
            "I20101",
            "Earned Leave",
            24,
            12,
            12
        ),

        # I20102
        (
            "I20102",
            "Casual Leave",
            12,
            5,
            7
        ),
        (
            "I20102",
            "Sick Leave",
            12,
            2,
            10
        ),
        (
            "I20102",
            "Earned Leave",
            24,
            8,
            16
        ),

        # I16003
        (
            "I16003",
            "Casual Leave",
            12,
            3,
            9
        ),
        (
            "I16003",
            "Sick Leave",
            12,
            1,
            11
        ),
        (
            "I16003",
            "Earned Leave",
            24,
            4,
            20
        ),

        # I20203
        (
            "I20203",
            "Casual Leave",
            12,
            2,
            10
        ),
        (
            "I20203",
            "Sick Leave",
            12,
            1,
            11
        ),
        (
            "I20203",
            "Earned Leave",
            24,
            6,
            18
        )
    ]

    cursor.executemany(
        """
        INSERT INTO leave_balances
        (
            employee_id,
            leave_type,
            allocated,
            used,
            remaining
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        balances
    )

    connection.commit()

    connection.close()


def seed_leave_history():

    connection = get_connection()

    cursor = connection.cursor()

    history = [

        (
            "I20101",
            "Casual Leave",
            "2026-02-10",
            "2026-02-11",
            2,
            "Approved",
            "Personal work"
        ),

        (
            "I20101",
            "Sick Leave",
            "2026-04-20",
            "2026-04-21",
            2,
            "Approved",
            "Medical"
        ),

        (
            "I20102",
            "Earned Leave",
            "2026-05-05",
            "2026-05-08",
            4,
            "Approved",
            "Vacation"
        )
    ]

    cursor.executemany(
        """
        INSERT INTO leave_history
        (
            employee_id,
            leave_type,
            start_date,
            end_date,
            days,
            status,
            reason
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        history
    )

    connection.commit()

    connection.close()


def seed_holidays():

    connection = get_connection()

    cursor = connection.cursor()

    holidays = [

        (
            "2026-01-26",
            "Republic Day"
        ),

        (
            "2026-08-15",
            "Independence Day"
        ),

        (
            "2026-10-02",
            "Gandhi Jayanti"
        ),

        (
            "2026-12-25",
            "Christmas"
        )
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO holidays
        (
            holiday_date,
            holiday_name
        )
        VALUES (?, ?)
        """,
        holidays
    )

    connection.commit()

    connection.close()


if __name__ == "__main__":

    initialize_database()

    seed_employees()

    seed_leave_balances()

    seed_leave_history()

    seed_holidays()

    print(
        "HR database seeded successfully."
    )