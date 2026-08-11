# Phase 13 – Notification Management

## 1. Phase Overview

Phase 13 implements the Notification Management module for the GramSeva
Smart Village Governance Platform.

The notification system allows the application to create, retrieve,
filter, update, and mark notifications as read for users.

Notifications can be associated with complaints and complaint escalations.

---

## 2. Objectives

The main objectives of Phase 13 were:

- Create a centralized notification system.
- Store notifications for individual users.
- Link notifications with complaints.
- Link notifications with complaint escalations.
- Support notification types.
- Track read/unread status.
- Store read timestamp.
- Provide user-specific notification APIs.
- Provide unread notification filtering.
- Provide mark-as-read functionality.
- Provide mark-all-as-read functionality.
- Maintain active/inactive notification state.
- Integrate the notification module with FastAPI.

---

## 3. Notification Database Design

A new `notifications` table was created.

### Table: notifications

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| user_id | Integer | User receiving the notification |
| complaint_id | Integer | Related complaint, nullable |
| escalation_id | Integer | Related escalation, nullable |
| title | VARCHAR(255) | Notification title |
| message | TEXT | Notification message |
| notification_type | VARCHAR(50) | Type of notification |
| is_read | Boolean | Read/unread status |
| read_at | DateTime | Time notification was read |
| is_active | Boolean | Active/inactive status |
| created_at | DateTime | Notification creation time |

---

## 4. Notification Relationships

The notification system supports relationships with:

- User
- Complaint
- Complaint Escalation

Foreign keys:

```text
notifications.user_id
        ↓
users.id