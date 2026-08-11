# Phase 14 – Complaint Assignment Management

## 1. Phase Overview

Phase 14 focuses on the Complaint Assignment Management module of the GramSeva backend.

The purpose of this module is to allow authorized administrators to assign complaints to responsible officers, view assignments, update assignment remarks, and deactivate assignments using a soft-delete mechanism.

The module also includes validation to prevent duplicate active assignments for the same complaint.

---

## 2. Objectives

The main objectives of Phase 14 are:

- Assign complaints to responsible officers.
- Prevent duplicate active assignments.
- Retrieve all active complaint assignments.
- Retrieve a specific assignment by ID.
- Update assignment remarks.
- Soft delete assignments.
- Protect assignment APIs using JWT authentication and admin authorization.
- Validate complaint and officer existence before assignment.
- Maintain assignment timestamps.
- Provide production-ready service-layer architecture.

---

## 3. Architecture

The Complaint Assignment module follows a layered architecture:

```text
API Router
    ↓
Service Layer
    ↓
SQLAlchemy ORM Model
    ↓
MySQL Database