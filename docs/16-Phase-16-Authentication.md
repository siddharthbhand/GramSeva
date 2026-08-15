# GramSeva – Phase 16 Documentation
## User Role Management & Intelligent SLA Escalation Hierarchy

**Project:** GramSeva – AI Powered Smart Village Governance Platform  
**Phase:** 16  
**Status:** Completed  
**Date:** August 2026

---

# 1. Phase 16 Objective

Phase 16 focused on strengthening the backend around **User Role Management** and making the **Intelligent Escalation & SLA Management** workflow operational.

### Main objectives

- Centralize application user roles.
- Improve admin user management.
- Validate user roles properly.
- Build configurable escalation hierarchy.
- Connect SLA breaches with automatic escalation.
- Automatically notify the authority receiving an escalation.
- Prevent duplicate escalation notifications.
- Stop escalation after the maximum configured level.
- Test the complete escalation workflow.
- Clean temporary test data.
- Complete Git commit and push after phase completion.

---

# 2. Starting Point

At the beginning of Phase 16, the project already had:

- FastAPI backend
- SQLAlchemy database integration
- User model
- JWT authentication
- Complaint management
- Complaint assignment
- Complaint history
- Complaint escalation model
- Notification model
- SLA automation foundation
- Admin role protection

The purpose of Phase 16 was to build on the existing architecture instead of recreating already completed functionality.

---

# 3. Centralized User Role System

A centralized role enum was created.

### File

`app/core/user_roles.py`

### Supported roles

```text
citizen
officer
department_head
admin