import hashlib

from database.employee_repository import (
    get_employee
)


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.

    For production, use Argon2/bcrypt
    or enterprise identity management.
    """

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def verify_password(
    password: str,
    password_hash: str
) -> bool:

    return (
        hash_password(password)
        == password_hash
    )


def authenticate_employee(
    employee_id: str,
    password: str
):
    """
    Authenticate an employee.

    Returns the employee record if valid.
    Otherwise returns None.
    """

    employee = get_employee(
        employee_id
    )

    if employee is None:
        return None

    if not employee["is_active"]:
        return None

    if not verify_password(
        password,
        employee["password_hash"]
    ):
        return None

    return employee