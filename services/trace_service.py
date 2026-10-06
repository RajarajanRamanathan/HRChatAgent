from datetime import datetime
from typing import Any


def create_trace():
    return {
        "start_time": datetime.now(),
        "events": []
    }


def add_trace_event(
    trace: dict,
    event_type: str,
    message: str,
    status: str = "success",
    metadata: dict[str, Any] | None = None
):
    event = {
        "timestamp": datetime.now(),
        "event_type": event_type,
        "message": message,
        "status": status,
        "metadata": metadata or {}
    }

    trace["events"].append(event)


def complete_trace(trace: dict):

    end_time = datetime.now()

    start_time = trace["start_time"]

    duration = (
        end_time - start_time
    ).total_seconds()

    trace["end_time"] = end_time

    trace["duration"] = duration

    return trace