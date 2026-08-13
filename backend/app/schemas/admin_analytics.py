from datetime import date

from pydantic import BaseModel


# =====================================================
# Complaint Statistics
# =====================================================

class ComplaintStatistics(BaseModel):
    total: int
    pending: int
    assigned: int
    in_progress: int
    resolved: int
    closed: int
    rejected: int
    reopened: int


# =====================================================
# User Statistics
# =====================================================

class UserStatistics(BaseModel):
    total: int
    citizens: int
    officers: int
    department_heads: int
    admins: int


# =====================================================
# SLA Statistics
# =====================================================

class SLAStatistics(BaseModel):
    tracked: int
    within_sla: int
    breached: int


# =====================================================
# Escalation Statistics
# =====================================================

class EscalationStatistics(BaseModel):
    total: int
    level_1: int
    level_2: int


# =====================================================
# Phase 17.2
# Status Analytics
# =====================================================

class StatusAnalytics(BaseModel):
    status: str
    count: int


# =====================================================
# Phase 17.2
# Priority Analytics
# =====================================================

class PriorityAnalytics(BaseModel):
    priority: str
    count: int


# =====================================================
# Phase 17.2
# Department Analytics
# =====================================================

class DepartmentAnalytics(BaseModel):
    department_id: int | None
    department_name: str
    count: int


# =====================================================
# Phase 17.2
# Complaint Trend
# =====================================================

class ComplaintTrend(BaseModel):
    date: date
    count: int


# =====================================================
# Phase 17.2
# Complete Complaint Analytics
# =====================================================

class ComplaintAnalytics(BaseModel):
    total: int
    by_status: list[StatusAnalytics]
    by_priority: list[PriorityAnalytics]
    by_department: list[DepartmentAnalytics]
    resolution_rate: float
    trend: list[ComplaintTrend]


# =====================================================
# Phase 17.3
# Officer Workload Analytics
# =====================================================

class OfficerWorkloadAnalytics(BaseModel):
    officer_id: int
    officer_name: str
    assigned: int
    pending: int
    in_progress: int
    resolved: int
    closed: int


# =====================================================
# Admin Dashboard Summary
# =====================================================

class AdminAnalyticsSummary(BaseModel):
    complaints: ComplaintStatistics
    users: UserStatistics
    departments: int
    sla: SLAStatistics
    escalations: EscalationStatistics