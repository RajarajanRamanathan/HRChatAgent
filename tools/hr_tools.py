from database.database import get_connection


# ---------------------------------------------------------
# EMPLOYEE PROFILE
# ---------------------------------------------------------

def get_employee_profile(employee_id: str):

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
            manager_id
        FROM employees
        WHERE employee_id = ?
          AND is_active = 1
        """,
        (employee_id,)
    )

    employee = cursor.fetchone()

    connection.close()

    if employee is None:

        return {
            "success": False,
            "message": "Employee not found."
        }

    return {
        "success": True,
        "employee": {
            "employee_id": employee["employee_id"],
            "name": employee["name"],
            "email": employee["email"],
            "department": employee["department"],
            "designation": employee["designation"],
            "join_date": employee["join_date"],
            "manager_id": employee["manager_id"]
        }
    }


# ---------------------------------------------------------
# LEAVE BALANCE
# ---------------------------------------------------------

def get_leave_balance(
    employee_id: str,
    leave_type: str = None
):

    connection = get_connection()
    cursor = connection.cursor()

    if leave_type:

        cursor.execute(
            """
            SELECT
                leave_type,
                allocated,
                used,
                remaining
            FROM leave_balances
            WHERE employee_id = ?
              AND LOWER(leave_type) = LOWER(?)
            """,
            (
                employee_id,
                leave_type
            )
        )

    else:

        cursor.execute(
            """
            SELECT
                leave_type,
                allocated,
                used,
                remaining
            FROM leave_balances
            WHERE employee_id = ?
            ORDER BY leave_type
            """,
            (employee_id,)
        )

    rows = cursor.fetchall()

    connection.close()

    if not rows:

        return {
            "success": False,
            "message": "No leave balance found."
        }

    balances = []

    for row in rows:

        balances.append(
            {
                "leave_type": row["leave_type"],
                "allocated": row["allocated"],
                "used": row["used"],
                "remaining": row["remaining"]
            }
        )

    return {
        "success": True,
        "employee_id": employee_id,
        "balances": balances
    }


# ---------------------------------------------------------
# LEAVE HISTORY
# ---------------------------------------------------------

def get_leave_history(
    employee_id: str,
    leave_type: str = None
):

    connection = get_connection()
    cursor = connection.cursor()

    if leave_type:

        cursor.execute(
            """
            SELECT
                leave_type,
                start_date,
                end_date,
                days,
                status,
                reason
            FROM leave_history
            WHERE employee_id = ?
              AND LOWER(leave_type) = LOWER(?)
            ORDER BY start_date DESC
            """,
            (
                employee_id,
                leave_type
            )
        )

    else:

        cursor.execute(
            """
            SELECT
                leave_type,
                start_date,
                end_date,
                days,
                status,
                reason
            FROM leave_history
            WHERE employee_id = ?
            ORDER BY start_date DESC
            """,
            (employee_id,)
        )

    rows = cursor.fetchall()

    connection.close()

    history = []

    for row in rows:

        history.append(
            {
                "leave_type": row["leave_type"],
                "start_date": row["start_date"],
                "end_date": row["end_date"],
                "days": row["days"],
                "status": row["status"],
                "reason": row["reason"]
            }
        )

    return {
        "success": True,
        "employee_id": employee_id,
        "history": history
    }


# ---------------------------------------------------------
# HOLIDAYS
# ---------------------------------------------------------

def get_holidays(year: int = None):

    connection = get_connection()
    cursor = connection.cursor()

    if year:

        cursor.execute(
            """
            SELECT
                holiday_date,
                holiday_name
            FROM holidays
            WHERE holiday_date LIKE ?
            ORDER BY holiday_date
            """,
            (f"{year}-%",)
        )

    else:

        cursor.execute(
            """
            SELECT
                holiday_date,
                holiday_name
            FROM holidays
            ORDER BY holiday_date
            """
        )

    rows = cursor.fetchall()

    connection.close()

    holidays = []

    for row in rows:

        holidays.append(
            {
                "date": row["holiday_date"],
                "name": row["holiday_name"]
            }
        )

    return {
        "success": True,
        "year": year,
        "holidays": holidays
    }


# ---------------------------------------------------------
# EMPLOYEE SUMMARY
# ---------------------------------------------------------

def get_employee_summary(employee_id: str):

    profile = get_employee_profile(
        employee_id
    )

    balance = get_leave_balance(
        employee_id
    )

    if not profile["success"]:

        return {
            "success": False,
            "message": profile["message"]
        }

    return {
        "success": True,
        "employee": profile["employee"],
        "leave_balances": balance.get(
            "balances",
            []
        )
    }