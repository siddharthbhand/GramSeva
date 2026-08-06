from datetime import datetime


class SLAUtils:

    @staticmethod
    def get_remaining_hours(sla_due_at: datetime | None) -> float:
        """
        Returns remaining hours before SLA expires.
        """

        if sla_due_at is None:
            return 0

        remaining = sla_due_at - datetime.utcnow()

        return remaining.total_seconds() / 3600

    @staticmethod
    def is_breached(sla_due_at: datetime | None) -> bool:
        """
        Returns True if SLA is breached.
        """

        if sla_due_at is None:
            return False

        return datetime.utcnow() > sla_due_at

    @staticmethod
    def is_near_breach(
        sla_due_at: datetime | None,
        threshold_hours: int = 4,
    ) -> bool:
        """
        Returns True if complaint is close to SLA deadline.
        Default threshold = 4 hours.
        """

        if sla_due_at is None:
            return False

        remaining = SLAUtils.get_remaining_hours(sla_due_at)

        return 0 < remaining <= threshold_hours

    @staticmethod
    def get_sla_status(sla_due_at: datetime | None) -> str:
        """
        Returns SLA status.
        """

        if sla_due_at is None:
            return "Unknown"

        if SLAUtils.is_breached(sla_due_at):
            return "Breached"

        if SLAUtils.is_near_breach(sla_due_at):
            return "Near Breach"

        return "Within SLA"