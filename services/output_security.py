import re


SENSITIVE_PATTERNS = [

    r"password",
    r"password_hash",
    r"secret",
    r"api[_\s-]?key",
    r"access[_\s-]?token",
    r"refresh[_\s-]?token",
    r"authorization"
]


def sanitize_response(
    response: str
) -> str:

    if not response:

        return response

    sanitized = response

    for pattern in SENSITIVE_PATTERNS:

        sanitized = re.sub(
            pattern,
            "[REDACTED]",
            sanitized,
            flags=re.IGNORECASE
        )

    return sanitized