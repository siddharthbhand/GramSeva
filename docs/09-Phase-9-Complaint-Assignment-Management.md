# Phase 9 – Complaint Assignment Management

## 1. Introduction

The Complaint Assignment Management module was developed to assign registered complaints to responsible officers for resolution. This module acts as a bridge between Complaint Management and the grievance resolution process.

To ensure security and reliability, JWT Authentication, Role-Based Access Control (RBAC), business validations, and database integrity checks were implemented. Only authorized administrators are allowed to assign complaints to officers.

---

# 2. Objective

The main objectives of this phase were:

- Develop the Complaint Assignment module.
- Assign complaints to authorized officers.
- Store assignment information securely in the database.
- Implement complete CRUD operations.
- Prevent duplicate complaint assignments.
- Implement Role-Based Access Control (RBAC).
- Secure APIs using JWT Authentication.
- Test all APIs using Swagger UI.
- Verify all records in the MySQL database.

---

# 3. Requirements

The following requirements were identified before implementation:

- Every complaint should be assignable to an officer.
- Only administrators should be able to assign complaints.
- Invalid complaints should not be assigned.
- Invalid officers should not receive assignments.
- Duplicate assignments should be prevented.
- Assignment details should be stored permanently.
- Every assignment should contain timestamps.

---

# 4. Files Created

The following project files were created during this phase.

## Model

```
app/models/complaint_assignment.py
```

## Schema

```
app/schemas/complaint_assignment.py
```

## Service

```
app/services/complaint_assignment_service.py
```

## API

```
app/api/complaint_assignments.py
```

---

# 5. Database Design

A new table named **complaint_assignments** was created.

| Column | Description |
|----------|-------------|
| id | Primary Key |
| complaint_id | Foreign Key referencing Complaint |
| officer_id | Assigned Officer |
| assigned_by | Administrator who assigned the complaint |
| remarks | Additional assignment remarks |
| is_active | Soft Delete flag |
| assigned_at | Assignment timestamp |
| created_at | Record creation timestamp |
| updated_at | Record update timestamp |

---

# 6. Relationships Implemented

The following SQLAlchemy relationships were implemented.

- Complaint → ComplaintAssignment
- User (Officer) → ComplaintAssignment
- User (Admin) → ComplaintAssignment

These relationships allow easy retrieval of assignment details along with complaint and officer information.

---

# 7. APIs Developed

The following REST APIs were implemented.

## Assign Complaint

```
POST /assignments/
```

Purpose:

Assign a complaint to an officer.

---

## Get All Assignments

```
GET /assignments/
```

Purpose:

Retrieve all active complaint assignments.

---

## Get Assignment By ID

```
GET /assignments/{assignment_id}
```

Purpose:

Retrieve details of a specific assignment.

---

## Update Assignment

```
PUT /assignments/{assignment_id}
```

Purpose:

Update officer information or assignment remarks.

---

## Delete Assignment

```
DELETE /assignments/{assignment_id}
```

Purpose:

Perform a soft delete on an assignment.

---

# 8. Business Logic Implemented

The following business rules were implemented.

- Verify that the complaint exists.
- Verify that the complaint is active.
- Verify that the assigned officer exists.
- Verify that the assigned officer is active.
- Prevent duplicate complaint assignments.
- Store assignment details in the database.
- Return the created assignment object.

---

# 9. Authentication and Authorization

The Complaint Assignment module was secured using JWT Authentication.

Role-Based Access Control (RBAC) was implemented.

Only users with the **Admin** role are authorized to:

- Create assignments
- Update assignments
- Delete assignments

Unauthorized users receive an access denied response.

---

# 10. Validations Implemented

The following validations were added.

- Complaint Not Found Validation
- Officer Not Found Validation
- Inactive Officer Validation
- Duplicate Assignment Validation
- Invalid Assignment ID Validation
- Already Deleted Assignment Validation

These validations improve system reliability and prevent invalid operations.

---

# 11. Problems Faced During Development

During implementation, several technical challenges were encountered.

## Problem 1

Relationship mapping errors occurred between ComplaintAssignment, Complaint, and User models.

### Solution

The issue was resolved by correctly configuring SQLAlchemy relationships using **relationship()**, **foreign_keys**, and **back_populates**.

---

## Problem 2

SQLAlchemy mapper initialization failed due to incorrect relationship definitions.

### Solution

The mapper configuration was corrected by defining proper bidirectional relationships across all related models.

---

## Problem 3

Swagger API returned **401 Unauthorized** while testing protected endpoints.

### Solution

JWT Authentication was configured correctly, and all protected APIs were tested after successful authorization.

---

## Problem 4

Duplicate complaint assignments were possible during initial implementation.

### Solution

Business validation was added to prevent assigning the same complaint multiple times.

---

# 12. Testing Performed

The following testing activities were completed.

## Swagger API Testing

Successfully tested:

- Create Assignment
- Get All Assignments
- Get Assignment By ID
- Update Assignment
- Delete Assignment

---

## Validation Testing

Successfully verified:

- Invalid Complaint ID
- Invalid Officer ID
- Unauthorized Access
- Duplicate Assignment Prevention
- Soft Delete Functionality

---

## Database Testing

The MySQL database was verified for:

- Successful record insertion
- Correct Complaint ID
- Correct Officer ID
- Proper Remarks storage
- Automatic Timestamp generation

---

# 13. Results

The Complaint Assignment module was successfully implemented with production-level architecture.

The module includes:

- Complete CRUD Operations
- JWT Authentication
- Role-Based Access Control
- Business Validations
- SQLAlchemy Relationships
- Swagger API Testing
- MySQL Verification
- Soft Delete Support

The module is fully integrated with the Complaint Management System and ready for production use.

---

# 14. Conclusion

Phase 9 successfully completed the Complaint Assignment Management module. The system now allows administrators to securely assign complaints to officers while maintaining data integrity, authentication, authorization, and business validations. This module forms an essential part of the grievance resolution workflow and provides a strong foundation for the Complaint Status Workflow and Intelligent Escalation features implemented in subsequent phases.