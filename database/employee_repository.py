from database.database import get_connection


def get_employee(
    employee_id: str
):
    """
    Retrieve an active employee by employee ID.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            employee_id,
            name,
            email,
            department,
            designation,
            join_date,
            manager_id,
            password_hash,
            is_active
        FROM employees
        WHERE employee_id = ?
          AND is_active = 1
        """,
        (employee_id,)
    )

    employee = cursor.fetchone()

    connection.close()

    return employee