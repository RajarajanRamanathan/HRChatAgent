from datetime import date, timedelta
from database.database import get_connection
from services.security_service import (
    validate_leave_type
)

# ---------------------------------------------------------
# DATE PARSING
# ---------------------------------------------------------

def parse_date(value: str) -> date:

    return date.fromisoformat(value)


# ---------------------------------------------------------
# HOLIDAY DATES
# ---------------------------------------------------------

def get_holiday_dates(
    start_date: date,
    end_date: date
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT holiday_date
        FROM holidays
        WHERE holiday_date BETWEEN ?
          AND ?
        """,
        (
            start_date.isoformat(),
            end_date.isoformat()
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return {
        date.fromisoformat(
            row["holiday_date"]
        )
        for row in rows
    }


# ---------------------------------------------------------
# WORKING DAYS
# ---------------------------------------------------------

def calculate_working_days(
    start_date: str,
    end_date: str
):

    start = parse_date(start_date)
    end = parse_date(end_date)

    if end < start:

        raise ValueError(
            "End date cannot be before start date."
        )

    holidays = get_holiday_dates(
        start,
        end
    )

    current_date = start

    working_days = 0
    weekend_days = 0
    holiday_days = 0

    while current_date <= end:

        if current_date.weekday() >= 5:

            weekend_days += 1

        elif current_date in holidays:

            holiday_days += 1

        else:

            working_days += 1

        current_date += timedelta(days=1)

    return {
        "success": True,
        "start_date": start_date,
        "end_date": end_date,
        "working_days": working_days,
        "weekend_days": weekend_days,
        "holiday_days": holiday_days,
        "total_calendar_days":
            (end - start).days + 1
    }


# ---------------------------------------------------------
# LEAVE DAYS
# ---------------------------------------------------------

def calculate_leave_days(
    start_date: str,
    end_date: str
):

    result = calculate_working_days(
        start_date,
        end_date
    )

    return {
        "success": True,
        "start_date": start_date,
        "end_date": end_date,
        "leave_days": result["working_days"],
        "weekend_days": result["weekend_days"],
        "holiday_days": result["holiday_days"]
    }


# ---------------------------------------------------------
# LEAVE BALANCE CHECK
# ---------------------------------------------------------

def check_leave_balance(
    employee_id: str,
    leave_type: str,
    required_days: float
):

    valid, message = validate_leave_type(
        leave_type
    )

    if not valid:

        return {
            "success": False,
            "eligible": False,
            "message": message
        }

    if required_days < 0:

        return {
            "success": False,
            "eligible": False,
            "message":
                "Required leave days cannot be negative."
        }

    if required_days > 365:

        return {
            "success": False,
            "eligible": False,
            "message":
                "Requested leave duration is invalid."
        }

    connection = get_connection()

    cursor = connection.cursor()

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

    row = cursor.fetchone()

    connection.close()

    if row is None:

        return {
            "success": False,
            "eligible": False,
            "message":
                f"No balance found for {leave_type}."
        }

    available = float(
        row["remaining"]
    )

    required = float(
        required_days
    )

    return {
        "success": True,
        "leave_type":
            row["leave_type"],
        "available_days":
            available,
        "required_days":
            required,
        "eligible":
            available >= required,
        "shortfall":
            max(
                0,
                required - available
            )
    }

# ---------------------------------------------------------
# PRORATED LEAVE
# ---------------------------------------------------------

def calculate_prorated_leave(
    join_date: str,
    annual_allocation: float,
    year: int
):

    joining_date = parse_date(
        join_date
    )

    if joining_date.year < year:

        return {
            "success": True,
            "year": year,
            "annual_allocation":
                annual_allocation,
            "prorated_allocation":
                annual_allocation,
            "months_eligible": 12
        }

    if joining_date.year > year:

        return {
            "success": True,
            "year": year,
            "annual_allocation":
                annual_allocation,
            "prorated_allocation": 0,
            "months_eligible": 0
        }

    remaining_months = (
        12 - joining_date.month + 1
    )

    prorated = (
        annual_allocation
        * remaining_months
        / 12
    )

    prorated = (
        round(prorated * 2)
        / 2
    )

    return {
        "success": True,
        "year": year,
        "annual_allocation":
            annual_allocation,
        "prorated_allocation":
            prorated,
        "months_eligible":
            remaining_months
    }


# ---------------------------------------------------------
# LEAVE ALLOCATION
# ---------------------------------------------------------

def get_leave_allocation(
    leave_type: str
):

    allocations = {
        "Casual Leave": 12,
        "Sick Leave": 12,
        "Earned Leave": 24
    }

    normalized = leave_type.strip().lower()

    for key, value in allocations.items():

        if key.lower() == normalized:

            return {
                "success": True,
                "leave_type": key,
                "annual_allocation": value
            }

    return {
        "success": False,
        "message":
            f"Unknown leave type: {leave_type}"
    }


# ---------------------------------------------------------
# LEAVE ELIGIBILITY
# ---------------------------------------------------------

def calculate_leave_eligibility(
    employee_id: str,
    leave_type: str,
    start_date: str,
    end_date: str
):

    leave_result = calculate_leave_days(
        start_date,
        end_date
    )

    if not leave_result["success"]:

        return leave_result

    required_days = (
        leave_result["leave_days"]
    )

    balance_result = check_leave_balance(
        employee_id,
        leave_type,
        required_days
    )

    if not balance_result["success"]:

        return balance_result

    eligible = (
        balance_result["eligible"]
    )

    if eligible:

        reason = (
            f"You have enough "
            f"{leave_type} balance."
        )

    else:

        reason = (
            f"You need "
            f"{required_days} days, "
            f"but only "
            f"{balance_result['available_days']} "
            f"days are available."
        )

    return {
        "success": True,
        "eligible": eligible,
        "employee_id": employee_id,
        "leave_type": leave_type,
        "start_date": start_date,
        "end_date": end_date,
        "required_days": required_days,
        "available_days":
            balance_result["available_days"],
        "shortfall":
            balance_result["shortfall"],
        "weekend_days":
            leave_result["weekend_days"],
        "holiday_days":
            leave_result["holiday_days"],
        "reason": reason
    }