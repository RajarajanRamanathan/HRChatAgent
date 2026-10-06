from dataclasses import dataclass

from services.security_service import (
    is_valid_employee_id
)


@dataclass
class HRContext:

    employee_id: str


def validate_context(
    context: HRContext
) -> str:

    if context is None:

        raise ValueError(
            "Authenticated HR context is required."
        )

    employee_id = context.employee_id

    if not employee_id:

        raise ValueError(
            "Authenticated employee ID is required."
        )

    employee_id = employee_id.strip().upper()

    if not is_valid_employee_id(
        employee_id
    ):

        raise ValueError(
            "Invalid authenticated employee ID."
        )

    return employee_id

def authorize_employee_request(
    context: HRContext,
    requested_employee_id: str
) -> str:

    authenticated_employee_id = (
        validate_context(context)
    )

    requested_employee_id = (
        requested_employee_id
        .strip()
        .upper()
    )

    if (
        requested_employee_id
        != authenticated_employee_id
    ):

        raise PermissionError(
            "Access denied. Employee information "
            "can only be accessed for the "
            "authenticated employee."
        )

    return authenticated_employee_id