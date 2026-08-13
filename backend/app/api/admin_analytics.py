from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.roles import require_admin
from app.schemas.admin_analytics import (
    AdminAnalyticsSummary,
    ComplaintAnalytics,
    OfficerWorkloadAnalytics,
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
# Phase 17.2
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
            "in the complaint trend."
        ),
    ),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """
    Return detailed complaint analytics
    for the admin dashboard.
    """

    return (
        AdminAnalyticsService
        .get_complaint_analytics(
            db=db,
            days=days,
        )
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