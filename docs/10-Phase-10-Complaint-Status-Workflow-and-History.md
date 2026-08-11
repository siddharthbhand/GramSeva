# Phase 10 – Complaint Status Workflow & Complaint History

## 1. Introduction

In this phase, the Complaint Status Workflow and Complaint History module were implemented to manage the complete lifecycle of complaints. Every complaint now follows a predefined workflow, ensuring that status changes occur only in the correct sequence.

Additionally, an audit trail mechanism was introduced to automatically record every status change, making the system transparent, traceable, and production-ready.

This phase significantly improves complaint tracking, accountability, and future reporting capabilities.

---

# 2. Objective

The primary objectives of this phase were:

- Implement Complaint Status Workflow.
- Define valid complaint status transitions.
- Prevent invalid status changes.
- Create Complaint History module.
- Automatically record every status change.
- Maintain complete audit logs.
- Provide APIs to retrieve complaint history.
- Secure all APIs using JWT Authentication and RBAC.
- Test all APIs using Swagger UI.
- Verify all data in the MySQL database.

---

# 3. Requirements

Before implementation, the following requirements were identified.

- Every complaint should follow a predefined lifecycle.
- Invalid status transitions should not be allowed.
- Every status update should be stored permanently.
- History records should include the previous status and new status.
- Every history record should store the user who performed the action.
- Complete complaint history should be available through APIs.
- Status updates should be secure and restricted to authorized users.

---

# 4. Files Created

The following files were created during this phase.

## Enum

```
app/core/enums.py
```

## Status Transition Rules

```
app/core/status_transition.py
```

## Complaint History Model

```
app/models/complaint_history.py
```

## Complaint History Schema

```
app/schemas/complaint_history.py
```

## Complaint History Service

```
app/services/complaint_history_service.py
```

## Complaint History API

```
app/api/complaint_history.py
```

---

# 5. Complaint Status Workflow

The following complaint lifecycle was implemented.

```
Pending
   ↓
Assigned
   ↓
In Progress
   ↓
Resolved
   ↓
Closed
```

Alternative workflow:

```
Resolved
   ↓
Reopened
   ↓
In Progress
```

The system validates every transition before updating the complaint status.

---

# 6. Complaint Status Enum

The following status values were implemented.

| Status |
|---------|
| Pending |
| Assigned |
| In Progress |
| Resolved |
| Closed |
| Rejected |
| Reopened |

Using Enum ensures consistency across the entire application and prevents invalid status values from being stored.

---

# 7. Complaint History Database Design

A new table named **complaint_history** was created.

| Column | Description |
|----------|-------------|
| id | Primary Key |
| complaint_id | Complaint Reference |
| old_status | Previous Complaint Status |
| new_status | Updated Complaint Status |
| changed_by | User who updated the status |
| remarks | Description of status change |
| created_at | Timestamp |

---

# 8. Relationships Implemented

The following relationships were added.

Complaint

↓

Complaint History

User

↓

Complaint History

These relationships allow complete tracking of every complaint status change.

---

# 9. APIs Developed

## Update Complaint Status

```
PUT /complaints/{complaint_id}/status
```

Purpose:

Update the complaint status after validating the workflow.

---

## Get Complaint History

```
GET /complaint-history/complaint/{complaint_id}
```

Purpose:

Retrieve the complete status history of a complaint.

---

## Get History By ID

```
GET /complaint-history/{history_id}
```

Purpose:

Retrieve a specific complaint history record.

---

# 10. Business Logic Implemented

The following business logic was implemented.

- Verify complaint exists.
- Verify complaint is active.
- Validate the requested status transition.
- Reject invalid transitions.
- Update complaint status.
- Automatically create Complaint History record.
- Store previous status.
- Store updated status.
- Store user ID.
- Store remarks.
- Store timestamp.
- Return updated complaint.

---

# 11. Authentication and Authorization

JWT Authentication was used to secure all APIs.

Role-Based Access Control (RBAC) was implemented.

Only authorized users are allowed to update complaint status.

Complaint History APIs are accessible only to authenticated users.

---

# 12. Validations Implemented

The following validations were implemented.

- Complaint Not Found Validation
- Invalid Status Transition Validation
- Same Status Update Prevention
- Unauthorized User Validation
- Invalid Complaint History ID Validation
- Authentication Validation

These validations ensure workflow integrity and data consistency.

---

# 13. Problems Faced During Development

During implementation several issues were encountered.

## Problem 1

Status values stored as String caused inconsistency.

### Solution

ComplaintStatus Enum was implemented throughout the application.

---

## Problem 2

Invalid complaint status updates were possible.

### Solution

A dedicated status transition validation module was developed to allow only valid workflow transitions.

---

## Problem 3

SQLAlchemy relationship errors occurred while connecting Complaint and ComplaintHistory models.

### Solution

Relationships were corrected using proper **relationship()**, **foreign_keys**, and **back_populates** configurations.

---

## Problem 4

Alembic migration for Complaint Status Enum required manual modification.

### Solution

The generated migration file was reviewed and updated before applying the migration successfully.

---

## Problem 5

Complaint History table migration was generated with an empty upgrade() function.

### Solution

The migration file was manually corrected, and the database version was synchronized using Alembic.

---

## Problem 6

Swagger returned **422 Unprocessable Entity** while updating complaint status.

### Solution

Pydantic schemas were updated to use ComplaintStatus Enum instead of plain strings.

---

## Problem 7

Mapper initialization failed because User model did not contain the required relationships.

### Solution

Missing relationships were added to User, Complaint, and ComplaintHistory models.

---

# 14. Testing Performed

## Swagger API Testing

Successfully tested:

- Update Complaint Status
- Get Complaint History
- Get History By ID

---

## Workflow Testing

Successfully verified:

- Pending → Assigned
- Assigned → In Progress
- In Progress → Resolved
- Resolved → Closed
- Resolved → Reopened
- Reopened → In Progress

Invalid transitions were rejected successfully.

---

## Validation Testing

Successfully tested:

- Invalid Complaint ID
- Invalid Status Transition
- Unauthorized Access
- Same Status Update
- Invalid History ID

---

## Database Testing

Verified in MySQL:

- Complaint status updated successfully.
- Complaint History created automatically.
- Old Status stored correctly.
- New Status stored correctly.
- Changed By stored correctly.
- Remarks stored correctly.
- Timestamp generated correctly.

---

# 15. Results

The Complaint Status Workflow and Complaint History module were successfully implemented.

The completed module includes:

- Complaint Status Enum
- Status Transition Rules
- Complaint Status API
- Complaint History Module
- Automatic Audit Logging
- Complaint History APIs
- JWT Authentication
- Role-Based Access Control
- Business Validations
- Swagger Testing
- MySQL Verification
- Alembic Migration

The module now provides a complete audit trail for every complaint and ensures that all complaint status updates follow a predefined workflow.

---

# 16. Conclusion

Phase 10 successfully introduced a production-ready Complaint Status Workflow and Complaint History system. The implementation guarantees secure status updates, maintains complete audit records, enforces valid workflow transitions, and provides transparency throughout the complaint lifecycle. This phase lays the foundation for the upcoming Intelligent SLA Management and Automatic Escalation modules.