from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.roles import require_admin
from app.schemas.admin_analytics import (
    AdminAnalyticsSummary,
    ComplaintAnalytics,
    EscalationAnalytics,
    OfficerWorkloadAnalytics,
    PendingComplaintAnalytics,
    SLAStatistics,
)
from app.services.admin_analytics_service import (
    AdminAnalyticsService,
)


router = APIRouter(
    prefix="/admin/analytics",
    tags=["Admin Analytics"],
)


# =====================================================
# Admin Dashboard Summary
# =====================================================

@router.get(
    "/summary",
    response_model=AdminAnalyticsSummary,
)
def get_admin_dashboard_summary(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """
    Return summary statistics for the admin dashboard.
    """

    return (
        AdminAnalyticsService
        .get_dashboard_summary(db)
    )


# =====================================================
# Phase 17.2 + Phase 17.6
# Complaint Analytics
# =====================================================

@router.get(
    "/complaints",
    response_model=ComplaintAnalytics,
)
def get_complaint_analytics(
    days: int = Query(
        default=30,
        ge=1,
        le=365,
        description=(
            "Number of days to include "
            "when no explicit date range is provided."
        ),
    ),
    start_date: date | None = Query(
        default=None,
        description=(
            "Start date for complaint analytics "
            "in YYYY-MM-DD format."
        ),
    ),
    end_date: date | None = Query(
        default=None,
        description=(
            "End date for complaint analytics "
            "in YYYY-MM-DD format."
        ),
    ),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """
    Return detailed complaint analytics
    for the admin dashboard.

    Supports:

    1. Existing days-based filtering:

       /admin/analytics/complaints?days=30

    2. Explicit date-range filtering:

       /admin/analytics/complaints
       ?start_date=2026-08-01
       &end_date=2026-08-15

    3. Only start_date:

       Uses start_date through today.

    4. Only end_date:

       Uses a 30-day period ending on end_date.

    Explicit date filters take priority over days.
    """

    # -------------------------------------------------
    # Validate explicit date range
    # -------------------------------------------------

    if (
        start_date is not None
        and end_date is not None
        and end_date < start_date
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "end_date cannot be earlier "
                "than start_date."
            ),
        )

    try:

        return (
            AdminAnalyticsService
            .get_complaint_analytics(
                db=db,
                days=days,
                start_date=start_date,
                end_date=end_date,
            )
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


# =====================================================
# Phase 17.3
# Officer Workload Analytics
# =====================================================

@router.get(
    "/officers",
    response_model=list[OfficerWorkloadAnalytics],
)
def get_officer_workload_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """
    Return workload statistics for all active officers.

    Only administrators can access this endpoint.
    """

    return (
        AdminAnalyticsService
        .get_officer_workload_analytics(
            db=db,
        )
    )


# =====================================================
# Phase 17.3
# SLA Analytics
# =====================================================

@router.get(
    "/sla",
    response_model=SLAStatistics,
)
def get_sla_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """
    Return SLA performance statistics
    for the admin dashboard.
    """

    return (
        AdminAnalyticsService
        .get_sla_statistics(db)
    )


# =====================================================
# Phase 17.4
# Escalation Analytics
# =====================================================

@router.get(
    "/escalations",
    response_model=EscalationAnalytics,
)
def get_escalation_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """
    Return detailed escalation analytics
    for the admin dashboard.

    Only administrators can access this endpoint.
    """

    return (
        AdminAnalyticsService
        .get_escalation_analytics(
            db=db,
        )
    )


# =====================================================
# Phase 17.5
# Pending & Overdue Complaint Analytics
# =====================================================

@router.get(
    "/pending",
    response_model=PendingComplaintAnalytics,
)
def get_pending_complaint_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """
    Return pending and overdue complaint analytics
    for the admin dashboard.

    Only administrators can access this endpoint.
    """

    return (
        AdminAnalyticsService
        .get_pending_complaint_analytics(
            db=db,
        )
    )