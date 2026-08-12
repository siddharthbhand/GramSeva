# Phase 14 – Complaint Assignment Management

## 1. Phase Overview

Phase 14 focuses on the Complaint Assignment Management module of the GramSeva backend.

The purpose of this module is to allow authorized administrators to assign complaints to responsible officers, view active assignments, retrieve individual assignments, update assignment remarks, and deactivate assignments using a soft-delete mechanism.

The module also includes validation to ensure that complaints and officers exist before an assignment is created and prevents duplicate active assignments for the same complaint.

---

## 2. Objectives

The main objectives of Phase 14 are:

- Assign complaints to responsible officers.
- Validate complaint existence before assignment.
- Validate officer existence before assignment.
- Prevent duplicate active assignments for the same complaint.
- Retrieve all active complaint assignments.
- Retrieve a specific assignment by ID.
- Update assignment remarks.
- Soft delete assignments.
- Protect assignment APIs using JWT authentication.
- Restrict assignment operations to authorized administrators.
- Store the administrator who created the assignment.
- Maintain assignment timestamps.
- Follow a layered service-based architecture.
- Provide a production-ready foundation for future complaint workflow management.

---

## 3. Architecture

The Complaint Assignment module follows a layered architecture:

```text
Client / Swagger UI
        ↓
FastAPI Router
        ↓
Authentication & Role Authorization
        ↓
Complaint Assignment Service
        ↓
SQLAlchemy ORM Model
        ↓
Database