import re
from typing import Optional


# =========================================================
# SECURITY CONSTANTS
# =========================================================

MAX_QUESTION_LENGTH = 2000

MAX_LEAVE_TYPE_LENGTH = 50

ALLOWED_LEAVE_TYPES = {
    "casual leave",
    "sick leave",
    "earned leave"
}


# =========================================================
# EMPLOYEE ID VALIDATION
# =========================================================

def is_valid_employee_id(
    employee_id: Optional[str]
) -> bool:

    if not employee_id:
        return False

    employee_id = employee_id.strip()

    return bool(
        re.fullmatch(
            r"EMP\d{4,10}",
            employee_id,
            re.IGNORECASE
        )
    )


# =========================================================
# QUESTION VALIDATION
# =========================================================

def validate_question(
    question: str
) -> tuple[bool, str]:

    if not question:

        return (
            False,
            "Please enter a question."
        )

    question = question.strip()

    if not question:

        return (
            False,
            "Please enter a question."
        )

    if len(question) > MAX_QUESTION_LENGTH:

        return (
            False,
            "Your question is too long. "
            "Please keep it under 2000 characters."
        )

    return (
        True,
        ""
    )


# =========================================================
# LEAVE TYPE VALIDATION
# =========================================================

def validate_leave_type(
    leave_type: str
) -> tuple[bool, str]:

    if not leave_type:

        return (
            False,
            "Leave type is required."
        )

    leave_type = leave_type.strip()

    if len(leave_type) > MAX_LEAVE_TYPE_LENGTH:

        return (
            False,
            "Invalid leave type."
        )

    if leave_type.lower() not in ALLOWED_LEAVE_TYPES:

        return (
            False,
            "Unsupported leave type."
        )

    return (
        True,
        ""
    )


# =========================================================
# EMPLOYEE ACCESS VALIDATION
# =========================================================

def validate_employee_access(
    authenticated_employee_id: str,
    requested_employee_id: str
) -> tuple[bool, str]:

    if not authenticated_employee_id:

        return (
            False,
            "Authenticated employee context is missing."
        )

    if not requested_employee_id:

        return (
            False,
            "Requested employee is missing."
        )

    authenticated_employee_id = (
        authenticated_employee_id.strip().upper()
    )

    requested_employee_id = (
        requested_employee_id.strip().upper()
    )

    if (
        authenticated_employee_id
        != requested_employee_id
    ):

        return (
            False,
            "Access denied. You can only access "
            "your own employee information."
        )

    return (
        True,
        ""
    )


# =========================================================
# PROMPT INJECTION DETECTION
# =========================================================

PROMPT_INJECTION_PATTERNS = [

    r"ignore\s+(all\s+)?previous\s+instructions",

    r"ignore\s+(all\s+)?above\s+instructions",

    r"disregard\s+(all\s+)?previous\s+instructions",

    r"forget\s+(all\s+)?previous\s+instructions",

    r"system\s+prompt",

    r"reveal\s+(your\s+)?instructions",

    r"show\s+(me\s+)?your\s+prompt",

    r"developer\s+message",

    r"jailbreak",

    r"bypass\s+security",

    r"disable\s+security",

    r"override\s+security",

    r"act\s+as\s+administrator",

    r"pretend\s+you\s+are\s+an?\s+admin",

    r"reveal\s+hidden\s+reasoning",

    r"show\s+your\s+chain\s+of\s+thought"
]


def detect_prompt_injection(
    question: str
) -> bool:

    if not question:

        return False

    normalized = question.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:

        if re.search(
            pattern,
            normalized
        ):

            return True

    return False


# =========================================================
# SECURITY CHECK
# =========================================================

def security_check(
    question: str
) -> tuple[bool, str]:

    valid, message = validate_question(
        question
    )

    if not valid:

        return (
            False,
            message
        )

    if detect_prompt_injection(
        question
    ):

        return (
            False,
            "I can't help with requests to bypass "
            "security controls or reveal internal "
            "instructions."
        )

    return (
        True,
        ""
    )