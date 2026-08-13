from datetime import datetime, timedelta, timezone

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.complaint_assignment import ComplaintAssignment
from app.models.complaint_escalation import ComplaintEscalation
from app.models.department import Department
from app.models.user import User


class AdminAnalyticsService:

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
    ) -> list[dict]:

        rows = (
            db.query(
                Complaint.status,
                func.count(Complaint.id),
            )
            .filter(
                Complaint.is_active == True,
            )
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
    ) -> list[dict]:

        rows = (
            db.query(
                Complaint.priority,
                func.count(Complaint.id),
            )
            .filter(
                Complaint.is_active == True,
            )
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
    ) -> list[dict]:

        rows = (
            db.query(
                Department.id,
                Department.name,
                func.count(Complaint.id),
            )
            .outerjoin(
                Complaint,
                Complaint.department_id == Department.id,
            )
            .filter(
                Department.is_active == True,
                (
                    (Complaint.is_active == True)
                    | Complaint.id.is_(None)
                ),
            )
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
    ) -> float:

        total = (
            db.query(func.count(Complaint.id))
            .filter(
                Complaint.is_active == True,
            )
            .scalar()
            or 0
        )

        if total == 0:
            return 0.0

        resolved_or_closed = (
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
            .scalar()
            or 0
        )

        return round(
            (resolved_or_closed / total) * 100,
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
    ) -> list[dict]:

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

        rows = (
            db.query(
                func.date(Complaint.created_at),
                func.count(Complaint.id),
            )
            .filter(
                Complaint.is_active == True,
                Complaint.created_at >= start_date,
            )
            .group_by(
                func.date(Complaint.created_at),
            )
            .order_by(
                func.date(Complaint.created_at).asc(),
            )
            .all()
        )

        trend_map = {
            complaint_date: count
            for complaint_date, count in rows
        }

        result = []

        for offset in range(days):

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
    # Phase 17.2
    # Complete Complaint Analytics
    # =====================================================

    @staticmethod
    def get_complaint_analytics(
        db: Session,
        days: int = 30,
    ) -> dict:

        total = (
            db.query(func.count(Complaint.id))
            .filter(
                Complaint.is_active == True,
            )
            .scalar()
            or 0
        )

        return {
            "total": total,
            "by_status": (
                AdminAnalyticsService
                .get_status_analytics(db)
            ),
            "by_priority": (
                AdminAnalyticsService
                .get_priority_analytics(db)
            ),
            "by_department": (
                AdminAnalyticsService
                .get_department_analytics(db)
            ),
            "resolution_rate": (
                AdminAnalyticsService
                .get_resolution_rate(db)
            ),
            "trend": (
                AdminAnalyticsService
                .get_complaint_trend(
                    db=db,
                    days=days,
                )
            ),
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
            db.query(func.count(Department.id))
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
            db.query(func.count(Complaint.id))
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
            db.query(func.count(Complaint.id))
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
            db.query(func.count(ComplaintEscalation.id))
            .filter(
                ComplaintEscalation.is_active == True,
            )
            .scalar()
            or 0
        )

        level_1 = (
            db.query(func.count(ComplaintEscalation.id))
            .filter(
                ComplaintEscalation.is_active == True,
                ComplaintEscalation.escalation_level == 1,
            )
            .scalar()
            or 0
        )

        level_2 = (
            db.query(func.count(ComplaintEscalation.id))
            .filter(
                ComplaintEscalation.is_active == True,
                ComplaintEscalation.escalation_level == 2,
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