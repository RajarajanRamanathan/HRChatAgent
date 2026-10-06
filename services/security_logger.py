import logging


logging.basicConfig(
    filename="hr_security.log",
    level=logging.WARNING,
    format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(message)s"
    )
)


security_logger = logging.getLogger(
    "hr_security"
)


def log_security_event(
    employee_id: str,
    event: str
):

    security_logger.warning(
        "Employee=%s Event=%s",
        employee_id,
        event
    )