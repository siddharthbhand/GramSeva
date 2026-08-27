from datetime import datetime, timezone


class SLAUtils:

    @staticmethod
    def _normalize_datetime(
        sla_due_at: datetime,
    ) -> datetime:
        """
        Normalize SLA datetime for safe comparison.

        Naive datetimes are treated as local application/database
        time because the existing MySQL SLA timestamps are stored
        without timezone information.

        Timezone-aware datetimes are converted to UTC.
        """

        if sla_due_at.tzinfo is None:
            return sla_due_at

        return sla_due_at.astimezone(
            timezone.utc
        ).replace(
            tzinfo=None
        )

    @staticmethod
    def _current_datetime() -> datetime:
        """
        Return the current local application time as a naive
        datetime so it can safely be compared with the existing
        MySQL SLA timestamps.
        """

        return datetime.now()

    @staticmethod
    def get_remaining_hours(
        sla_due_at: datetime | None,
    ) -> float:
        """
        Return remaining hours before SLA expires.
        """

        if sla_due_at is None:
            return 0.0

        normalized_due_at = (
            SLAUtils._normalize_datetime(
                sla_due_at
            )
        )

        remaining = (
            normalized_due_at
            - SLAUtils._current_datetime()
        )

        return (
            remaining.total_seconds()
            / 3600
        )

    @staticmethod
    def is_breached(
        sla_due_at: datetime | None,
    ) -> bool:
        """
        Return True when the SLA deadline has passed.
        """

        if sla_due_at is None:
            return False

        normalized_due_at = (
            SLAUtils._normalize_datetime(
                sla_due_at
            )
        )

        return (
            SLAUtils._current_datetime()
            > normalized_due_at
        )

    @staticmethod
    def is_near_breach(
        sla_due_at: datetime | None,
        threshold_hours: int = 4,
    ) -> bool:
        """
        Return True when the complaint is within the
        configured near-breach threshold.
        """

        if sla_due_at is None:
            return False

        remaining = (
            SLAUtils.get_remaining_hours(
                sla_due_at
            )
        )

        return (
            0 < remaining <= threshold_hours
        )

    @staticmethod
    def get_sla_status(
        sla_due_at: datetime | None,
    ) -> str:
        """
        Return the current SLA status.
        """

        if sla_due_at is None:
            return "Unknown"

        if SLAUtils.is_breached(
            sla_due_at
        ):
            return "Breached"

        if SLAUtils.is_near_breach(
            sla_due_at
        ):
            return "Near Breach"

        return "Within SLA"