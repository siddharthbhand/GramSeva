from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =====================================================
# Create Notification
# =====================================================

class NotificationCreate(BaseModel):

    user_id: int

    complaint_id: Optional[int] = None

    escalation_id: Optional[int] = None

    title: str

    message: str

    notification_type: str


# =====================================================
# Update Notification
# =====================================================

class NotificationUpdate(BaseModel):

    title: Optional[str] = None

    message: Optional[str] = None

    notification_type: Optional[str] = None

    is_read: Optional[bool] = None

    is_active: Optional[bool] = None


# =====================================================
# Notification Response
# =====================================================

class NotificationResponse(BaseModel):

    id: int

    user_id: int

    complaint_id: Optional[int]

    escalation_id: Optional[int]

    title: str

    message: str

    notification_type: str

    is_read: bool

    read_at: Optional[datetime]

    is_active: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# =====================================================
# Notification List Response
# =====================================================

class NotificationListResponse(BaseModel):

    id: int

    user_id: int

    title: str

    message: str

    notification_type: str

    is_read: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# =====================================================
# Mark Notification As Read Response
# =====================================================

class NotificationReadResponse(BaseModel):

    id: int

    is_read: bool

    read_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True,
    )