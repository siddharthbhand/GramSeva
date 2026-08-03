from sqlalchemy.orm import Session

from app.models.complaint_history import ComplaintHistory
from app.core.enums import ComplaintStatus


class ComplaintHistoryService:

    @staticmethod
    def create_history(
        db: Session,
        complaint_id: int,
        old_status: ComplaintStatus,
        new_status: ComplaintStatus,
        changed_by: int,
        remarks: str | None = None,
    ):

        history = ComplaintHistory(
            complaint_id=complaint_id,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by,
            remarks=remarks,
        )

        db.add(history)
        db.commit()
        db.refresh(history)

        return history