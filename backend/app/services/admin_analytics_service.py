from datetime import (
    date,
    datetime,
    time,
    timedelta,
    timezone,
)

from sqlalchemy import (
    case,
    exists,
    func,
)
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.complaint_assignment import ComplaintAssignment
from app.models.complaint_escalation import ComplaintEscalation
from app.models.department import Department
from app.models.user import User


class AdminAnalyticsService:

    # =====================================================
    # Phase 17.6
    # Date Filter Helper
    # =====================================================

    @staticmethod
    def _build_date_filters(
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> tuple[datetime | None, datetime | None]:

        if start_date is None and end_date is None:
            return None, None

        # -------------------------------------------------
        # If only end_date is provided
        # use a 30-day range ending on end_date.
        # -------------------------------------------------

        if start_date is None and end_date is not None:
            start_date = (
                end_date
                - timedelta(days=29)
            )

        # -------------------------------------------------
        # If only start_date is provided
        # use start_date through today.
        # -------------------------------------------------

        if start_date is not None and end_date is None:
            end_date = (
                datetime.now(
                    timezone.utc
                ).date()
            )

        # -------------------------------------------------
        # Validate date range
        # -------------------------------------------------

        if end_date < start_date:
            raise ValueError(
                "end_date cannot be earlier than start_date."
            )

        # -------------------------------------------------
        # Convert date boundaries into datetime boundaries.
        #
        # Start:
        #   00:00:00 on start_date
        #
        # End:
        #   00:00:00 on the day after end_date
        #
        # Using an exclusive end boundary ensures that the
        # complete end_date is included.
        # -------------------------------------------------

        start_datetime = datetime.combine(
            start_date,
            time.min,
        )

        end_datetime = datetime.combine(
            end_date
            + timedelta(days=1),
            time.min,
        )

        return (
            start_datetime,
            end_datetime,
        )

    # =====================================================
    # Complaint Statistics
    # =====================================================

    @staticmethod
    def get_complaint_statistics(
        db: Session,
    ) -> dict:

        total = (
            db.query(func.count(Complaint.id))
            .filter(
                Complaint.is_active == True,
            )
            .scalar()
            or 0
        )

        pending = (
            db.query(func.count(Complaint.id))
            .filter(
                Complaint.is_active == True,
                Complaint.status == "PENDING",
            )
            .scalar()
            or 0
        )

        assigned = (
            db.query(func.count(Complaint.id))
            .filter(
                Complaint.is_active == True,
                Complaint.status == "ASSIGNED",
            )
            .scalar()
            or 0
        )

        in_progress = (
            db.query(func.count(Complaint.id))
            .filter(
                Complaint.is_active == True,
                Complaint.status == "IN_PROGRESS",
            )
            .scalar()
            or 0
        )

        resolved = (
            db.query(func.count(Complaint.id))
            .filter(
                Complaint.is_active == True,
                Complaint.status == "RESOLVED",
            )
            .scalar()
            or 0
        )

        closed = (
            db.query(func.count(Complaint.id))
            .filter(
                Complaint.is_active == True,
                Complaint.status == "CLOSED",
            )
            .scalar()
            or 0
        )

        rejected = (
            db.query(func.count(Complaint.id))
            .filter(
                Complaint.is_active == True,
                Complaint.status == "REJECTED",
            )
            .scalar()
            or 0
        )

        reopened = (
            db.query(func.count(Complaint.id))
            .filter(
                Complaint.is_active == True,
                Complaint.status == "REOPENED",
            )
            .scalar()
            or 0
        )

        return {
            "total": total,
            "pending": pending,
            "assigned": assigned,
            "in_progress": in_progress,
            "resolved": resolved,
            "closed": closed,
            "rejected": rejected,
            "reopened": reopened,
        }

    # =====================================================
    # Phase 17.2
    # Status-wise Complaint Analytics
    # =====================================================

    @staticmethod
    def get_status_analytics(
        db: Session,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[dict]:

        query = (
            db.query(
                Complaint.status,
                func.count(Complaint.id),
            )
            .filter(
                Complaint.is_active == True,
            )
        )

        if start_datetime is not None:
            query = query.filter(
                Complaint.created_at >= start_datetime,
            )

        if end_datetime is not None:
            query = query.filter(
                Complaint.created_at < end_datetime,
            )

        rows = (
            query
            .group_by(
                Complaint.status,
            )
            .order_by(
                Complaint.status,
            )
            .all()
        )

        return [
            {
                "status": (
                    status.value
                    if hasattr(status, "value")
                    else str(status)
                ),
                "count": count,
            }
            for status, count in rows
        ]

    # =====================================================
    # Phase 17.2
    # Priority-wise Complaint Analytics
    # =====================================================

    @staticmethod
    def get_priority_analytics(
        db: Session,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[dict]:

        query = (
            db.query(
                Complaint.priority,
                func.count(Complaint.id),
            )
            .filter(
                Complaint.is_active == True,
            )
        )

        if start_datetime is not None:
            query = query.filter(
                Complaint.created_at >= start_datetime,
            )

        if end_datetime is not None:
            query = query.filter(
                Complaint.created_at < end_datetime,
            )

        rows = (
            query
            .group_by(
                Complaint.priority,
            )
            .order_by(
                Complaint.priority,
            )
            .all()
        )

        return [
            {
                "priority": priority,
                "count": count,
            }
            for priority, count in rows
        ]

    # =====================================================
    # Phase 17.2
    # Department-wise Complaint Analytics
    # =====================================================

    @staticmethod
    def get_department_analytics(
        db: Session,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[dict]:

        query = (
            db.query(
                Department.id,
                Department.name,
                func.count(Complaint.id),
            )
            .outerjoin(
                Complaint,
                Complaint.department_id
                == Department.id,
            )
            .filter(
                Department.is_active == True,
                (
                    (Complaint.is_active == True)
                    | Complaint.id.is_(None)
                ),
            )
        )

        if start_datetime is not None:
            query = query.filter(
                (
                    Complaint.created_at
                    >= start_datetime
                )
                | Complaint.id.is_(None)
            )

        if end_datetime is not None:
            query = query.filter(
                (
                    Complaint.created_at
                    < end_datetime
                )
                | Complaint.id.is_(None)
            )

        rows = (
            query
            .group_by(
                Department.id,
                Department.name,
            )
            .order_by(
                Department.name.asc(),
            )
            .all()
        )

        return [
            {
                "department_id": department_id,
                "department_name": department_name,
                "count": count,
            }
            for (
                department_id,
                department_name,
                count,
            ) in rows
        ]

    # =====================================================
    # Phase 17.2
    # Resolution Rate
    # =====================================================

    @staticmethod
    def get_resolution_rate(
        db: Session,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> float:

        total_query = (
            db.query(func.count(Complaint.id))
            .filter(
                Complaint.is_active == True,
            )
        )

        if start_datetime is not None:
            total_query = total_query.filter(
                Complaint.created_at >= start_datetime,
            )

        if end_datetime is not None:
            total_query = total_query.filter(
                Complaint.created_at < end_datetime,
            )

        total = (
            total_query.scalar()
            or 0
        )

        if total == 0:
            return 0.0

        resolved_query = (
            db.query(func.count(Complaint.id))
            .filter(
                Complaint.is_active == True,
                Complaint.status.in_(
                    [
                        "RESOLVED",
                        "CLOSED",
                    ]
                ),
            )
        )

        if start_datetime is not None:
            resolved_query = resolved_query.filter(
                Complaint.created_at >= start_datetime,
            )

        if end_datetime is not None:
            resolved_query = resolved_query.filter(
                Complaint.created_at < end_datetime,
            )

        resolved_or_closed = (
            resolved_query.scalar()
            or 0
        )

        return round(
            (
                resolved_or_closed
                / total
            ) * 100,
            2,
        )

    # =====================================================
    # Phase 17.2
    # Complaint Trend
    # =====================================================

    @staticmethod
    def get_complaint_trend(
        db: Session,
        days: int = 30,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[dict]:

        # -------------------------------------------------
        # Explicit date range
        # -------------------------------------------------

        if (
            start_datetime is not None
            and end_datetime is not None
        ):

            start_date = (
                start_datetime.date()
            )

            end_date = (
                end_datetime
                - timedelta(days=1)
            ).date()

            trend_days = (
                end_date
                - start_date
            ).days + 1

        # -------------------------------------------------
        # Existing days-based behavior
        # -------------------------------------------------

        else:

            if days < 1:
                days = 30

            now_utc = datetime.now(
                timezone.utc
            ).replace(
                tzinfo=None,
            )

            start_date = (
                now_utc
                - timedelta(days=days - 1)
            ).date()

            end_date = (
                now_utc.date()
            )

            trend_days = days

            start_datetime = datetime.combine(
                start_date,
                time.min,
            )

            end_datetime = datetime.combine(
                end_date
                + timedelta(days=1),
                time.min,
            )

        rows = (
            db.query(
                func.date(
                    Complaint.created_at
                ),
                func.count(
                    Complaint.id
                ),
            )
            .filter(
                Complaint.is_active == True,
                Complaint.created_at >= start_datetime,
                Complaint.created_at < end_datetime,
            )
            .group_by(
                func.date(
                    Complaint.created_at
                ),
            )
            .order_by(
                func.date(
                    Complaint.created_at
                ).asc(),
            )
            .all()
        )

        trend_map = {
            complaint_date: count
            for complaint_date, count in rows
        }

        result = []

        for offset in range(
            trend_days
        ):

            current_date = (
                start_date
                + timedelta(days=offset)
            )

            result.append(
                {
                    "date": current_date,
                    "count": trend_map.get(
                        current_date,
                        0,
                    ),
                }
            )

        return result

    # =====================================================
    # Phase 17.2 + Phase 17.6
    # Complete Complaint Analytics
    # =====================================================

    @staticmethod
    def get_complaint_analytics(
        db: Session,
        days: int = 30,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> dict:

        # -------------------------------------------------
        # Resolve date range
        # -------------------------------------------------

        if (
            start_date is not None
            or end_date is not None
        ):

            (
                start_datetime,
                end_datetime,
            ) = (
                AdminAnalyticsService
                ._build_date_filters(
                    start_date=start_date,
                    end_date=end_date,
                )
            )

        else:

            if days < 1:
                days = 30

            now_utc = datetime.now(
                timezone.utc
            ).replace(
                tzinfo=None,
            )

            start_date = (
                now_utc
                - timedelta(days=days - 1)
            ).date()

            end_date = (
                now_utc.date()
            )

            start_datetime = datetime.combine(
                start_date,
                time.min,
            )

            end_datetime = datetime.combine(
                end_date
                + timedelta(days=1),
                time.min,
            )

        # -------------------------------------------------
        # Total complaints
        # -------------------------------------------------

        total = (
            db.query(
                func.count(
                    Complaint.id
                )
            )
            .filter(
                Complaint.is_active == True,
                Complaint.created_at >= start_datetime,
                Complaint.created_at < end_datetime,
            )
            .scalar()
            or 0
        )

        # -------------------------------------------------
        # Complaint trend
        # -------------------------------------------------

        trend = (
            AdminAnalyticsService
            .get_complaint_trend(
                db=db,
                days=days,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
            )
        )

        # -------------------------------------------------
        # Complete analytics
        # -------------------------------------------------

        return {
            "total": total,

            "by_status": (
                AdminAnalyticsService
                .get_status_analytics(
                    db=db,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                )
            ),

            "by_priority": (
                AdminAnalyticsService
                .get_priority_analytics(
                    db=db,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                )
            ),

            "by_department": (
                AdminAnalyticsService
                .get_department_analytics(
                    db=db,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                )
            ),

            "resolution_rate": (
                AdminAnalyticsService
                .get_resolution_rate(
                    db=db,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                )
            ),

            "trend": trend,
        }

    # =====================================================
    # Phase 17.3
    # Officer Workload Analytics
    # =====================================================

    @staticmethod
    def get_officer_workload_analytics(
        db: Session,
    ) -> list[dict]:
        """
        Return workload statistics for all active officers.

        Only active assignments and active complaints are
        included in the workload calculation.

        Workload is grouped by complaint status:

        ASSIGNED
        PENDING
        IN_PROGRESS
        RESOLVED
        CLOSED
        """

        rows = (
            db.query(
                User.id,
                User.full_name,

                func.coalesce(
                    func.sum(
                        case(
                            (
                                Complaint.status
                                == "ASSIGNED",
                                1,
                            ),
                            else_=0,
                        )
                    ),
                    0,
                ).label("assigned"),

                func.coalesce(
                    func.sum(
                        case(
                            (
                                Complaint.status
                                == "PENDING",
                                1,
                            ),
                            else_=0,
                        )
                    ),
                    0,
                ).label("pending"),

                func.coalesce(
                    func.sum(
                        case(
                            (
                                Complaint.status
                                == "IN_PROGRESS",
                                1,
                            ),
                            else_=0,
                        )
                    ),
                    0,
                ).label("in_progress"),

                func.coalesce(
                    func.sum(
                        case(
                            (
                                Complaint.status
                                == "RESOLVED",
                                1,
                            ),
                            else_=0,
                        )
                    ),
                    0,
                ).label("resolved"),

                func.coalesce(
                    func.sum(
                        case(
                            (
                                Complaint.status
                                == "CLOSED",
                                1,
                            ),
                            else_=0,
                        )
                    ),
                    0,
                ).label("closed"),
            )
            .outerjoin(
                ComplaintAssignment,
                (
                    ComplaintAssignment.officer_id
                    == User.id
                )
                & (
                    ComplaintAssignment.is_active
                    == True
                ),
            )
            .outerjoin(
                Complaint,
                (
                    Complaint.id
                    == ComplaintAssignment.complaint_id
                )
                & (
                    Complaint.is_active
                    == True
                ),
            )
            .filter(
                User.is_active == True,
                User.role == "officer",
            )
            .group_by(
                User.id,
                User.full_name,
            )
            .order_by(
                User.full_name.asc(),
            )
            .all()
        )

        return [
            {
                "officer_id": officer_id,
                "officer_name": officer_name,
                "assigned": int(
                    assigned or 0
                ),
                "pending": int(
                    pending or 0
                ),
                "in_progress": int(
                    in_progress or 0
                ),
                "resolved": int(
                    resolved or 0
                ),
                "closed": int(
                    closed or 0
                ),
            }
            for (
                officer_id,
                officer_name,
                assigned,
                pending,
                in_progress,
                resolved,
                closed,
            ) in rows
        ]

    # =====================================================
    # User Statistics
    # =====================================================

    @staticmethod
    def get_user_statistics(
        db: Session,
    ) -> dict:

        total = (
            db.query(func.count(User.id))
            .filter(
                User.is_active == True,
            )
            .scalar()
            or 0
        )

        citizens = (
            db.query(func.count(User.id))
            .filter(
                User.is_active == True,
                User.role == "citizen",
            )
            .scalar()
            or 0
        )

        officers = (
            db.query(func.count(User.id))
            .filter(
                User.is_active == True,
                User.role == "officer",
            )
            .scalar()
            or 0
        )

        department_heads = (
            db.query(func.count(User.id))
            .filter(
                User.is_active == True,
                User.role == "department_head",
            )
            .scalar()
            or 0
        )

        admins = (
            db.query(func.count(User.id))
            .filter(
                User.is_active == True,
                User.role == "admin",
            )
            .scalar()
            or 0
        )

        return {
            "total": total,
            "citizens": citizens,
            "officers": officers,
            "department_heads": department_heads,
            "admins": admins,
        }

    # =====================================================
    # Department Statistics
    # =====================================================

    @staticmethod
    def get_department_count(
        db: Session,
    ) -> int:

        return (
            db.query(
                func.count(
                    Department.id
                )
            )
            .filter(
                Department.is_active == True,
            )
            .scalar()
            or 0
        )

    # =====================================================
    # SLA Statistics
    # =====================================================

    @staticmethod
    def get_sla_statistics(
        db: Session,
    ) -> dict:

        tracked = (
            db.query(
                func.count(
                    Complaint.id
                )
            )
            .filter(
                Complaint.is_active == True,
                Complaint.sla_due_at.isnot(None),
            )
            .scalar()
            or 0
        )

        now_utc = datetime.now(
            timezone.utc
        ).replace(
            tzinfo=None
        )

        breached = (
            db.query(
                func.count(
                    Complaint.id
                )
            )
            .filter(
                Complaint.is_active == True,
                Complaint.sla_due_at.isnot(None),
                Complaint.sla_due_at < now_utc,
            )
            .scalar()
            or 0
        )

        within_sla = max(
            tracked - breached,
            0,
        )

        return {
            "tracked": tracked,
            "within_sla": within_sla,
            "breached": breached,
        }

    # =====================================================
    # Escalation Statistics
    # =====================================================

    @staticmethod
    def get_escalation_statistics(
        db: Session,
    ) -> dict:

        total = (
            db.query(
                func.count(
                    ComplaintEscalation.id
                )
            )
            .filter(
                ComplaintEscalation.is_active
                == True,
            )
            .scalar()
            or 0
        )

        level_1 = (
            db.query(
                func.count(
                    ComplaintEscalation.id
                )
            )
            .filter(
                ComplaintEscalation.is_active
                == True,
                ComplaintEscalation.escalation_level
                == 1,
            )
            .scalar()
            or 0
        )

        level_2 = (
            db.query(
                func.count(
                    ComplaintEscalation.id
                )
            )
            .filter(
                ComplaintEscalation.is_active
                == True,
                ComplaintEscalation.escalation_level
                == 2,
            )
            .scalar()
            or 0
        )

        return {
            "total": total,
            "level_1": level_1,
            "level_2": level_2,
        }

    # =====================================================
    # Phase 17.4
    # Detailed Escalation Analytics
    # =====================================================

    @staticmethod
    def get_escalation_analytics(
        db: Session,
    ) -> dict:
        """
        Return detailed escalation analytics
        for the admin dashboard.

        Includes:
        - Total escalations
        - Active escalations
        - Inactive escalations
        - Level 1 escalations
        - Level 2 escalations

        Total includes both active and inactive records.

        Level-wise counts include only active
        escalation records.
        """

        total = (
            db.query(
                func.count(
                    ComplaintEscalation.id
                )
            )
            .scalar()
            or 0
        )

        active = (
            db.query(
                func.count(
                    ComplaintEscalation.id
                )
            )
            .filter(
                ComplaintEscalation.is_active
                == True,
            )
            .scalar()
            or 0
        )

        inactive = (
            db.query(
                func.count(
                    ComplaintEscalation.id
                )
            )
            .filter(
                ComplaintEscalation.is_active
                == False,
            )
            .scalar()
            or 0
        )

        level_1 = (
            db.query(
                func.count(
                    ComplaintEscalation.id
                )
            )
            .filter(
                ComplaintEscalation.is_active
                == True,
                ComplaintEscalation.escalation_level
                == 1,
            )
            .scalar()
            or 0
        )

        level_2 = (
            db.query(
                func.count(
                    ComplaintEscalation.id
                )
            )
            .filter(
                ComplaintEscalation.is_active
                == True,
                ComplaintEscalation.escalation_level
                == 2,
            )
            .scalar()
            or 0
        )

        return {
            "total": total,
            "active": active,
            "inactive": inactive,
            "level_1": level_1,
            "level_2": level_2,
        }

    # =====================================================
    # Phase 17.5
    # Pending & Overdue Complaint Analytics
    # =====================================================

    @staticmethod
    def get_pending_complaint_analytics(
        db: Session,
    ) -> dict:
        """
        Return pending and overdue complaint analytics
        for the admin dashboard.

        Includes:

        - Total pending complaints
        - Pending complaints with an active assignment
        - Pending complaints without an active assignment
        - Pending complaints currently within SLA
        - Pending complaints that are overdue

        Only active complaints are included.
        """

        now_utc = datetime.now(
            timezone.utc
        ).replace(
            tzinfo=None,
        )

        total_pending = (
            db.query(
                func.count(
                    Complaint.id
                )
            )
            .filter(
                Complaint.is_active == True,
                Complaint.status == "PENDING",
            )
            .scalar()
            or 0
        )

        assigned_pending = (
            db.query(
                func.count(
                    Complaint.id
                )
            )
            .filter(
                Complaint.is_active == True,
                Complaint.status == "PENDING",
                exists().where(
                    (
                        ComplaintAssignment.complaint_id
                        == Complaint.id
                    )
                    & (
                        ComplaintAssignment.is_active
                        == True
                    )
                ),
            )
            .scalar()
            or 0
        )

        unassigned_pending = (
            db.query(
                func.count(
                    Complaint.id
                )
            )
            .filter(
                Complaint.is_active == True,
                Complaint.status == "PENDING",
                ~exists().where(
                    (
                        ComplaintAssignment.complaint_id
                        == Complaint.id
                    )
                    & (
                        ComplaintAssignment.is_active
                        == True
                    )
                ),
            )
            .scalar()
            or 0
        )

        within_sla = (
            db.query(
                func.count(
                    Complaint.id
                )
            )
            .filter(
                Complaint.is_active == True,
                Complaint.status == "PENDING",
                Complaint.sla_due_at.isnot(None),
                Complaint.sla_due_at >= now_utc,
                Complaint.is_sla_breached == False,
            )
            .scalar()
            or 0
        )

        overdue = (
            db.query(
                func.count(
                    Complaint.id
                )
            )
            .filter(
                Complaint.is_active == True,
                Complaint.status == "PENDING",
                (
                    (
                        Complaint.sla_due_at.isnot(None)
                        & (
                            Complaint.sla_due_at
                            < now_utc
                        )
                    )
                    | (
                        Complaint.is_sla_breached
                        == True
                    )
                ),
            )
            .scalar()
            or 0
        )

        return {
            "total_pending": int(
                total_pending
            ),
            "assigned_pending": int(
                assigned_pending
            ),
            "unassigned_pending": int(
                unassigned_pending
            ),
            "within_sla": int(
                within_sla
            ),
            "overdue": int(
                overdue
            ),
        }

    # =====================================================
    # Complete Admin Dashboard Summary
    # =====================================================

    @staticmethod
    def get_dashboard_summary(
        db: Session,
    ) -> dict:

        return {
            "complaints": (
                AdminAnalyticsService
                .get_complaint_statistics(db)
            ),
            "users": (
                AdminAnalyticsService
                .get_user_statistics(db)
            ),
            "departments": (
                AdminAnalyticsService
                .get_department_count(db)
            ),
            "sla": (
                AdminAnalyticsService
                .get_sla_statistics(db)
            ),
            "escalations": (
                AdminAnalyticsService
                .get_escalation_statistics(db)
            ),
        }