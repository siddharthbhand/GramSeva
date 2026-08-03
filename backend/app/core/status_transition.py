from app.core.enums import ComplaintStatus


ALLOWED_STATUS_TRANSITIONS = {
    ComplaintStatus.PENDING: [
        ComplaintStatus.ASSIGNED,
        ComplaintStatus.REJECTED,
    ],

    ComplaintStatus.ASSIGNED: [
        ComplaintStatus.IN_PROGRESS,
    ],

    ComplaintStatus.IN_PROGRESS: [
        ComplaintStatus.RESOLVED,
    ],

    ComplaintStatus.RESOLVED: [
        ComplaintStatus.CLOSED,
        ComplaintStatus.REOPENED,
    ],

    ComplaintStatus.REOPENED: [
        ComplaintStatus.IN_PROGRESS,
    ],

    ComplaintStatus.CLOSED: [],

    ComplaintStatus.REJECTED: [],
}


def is_valid_transition(current_status, new_status):
    """
    Returns True if status transition is allowed.
    """

    return new_status in ALLOWED_STATUS_TRANSITIONS.get(
        current_status,
        [],
    )