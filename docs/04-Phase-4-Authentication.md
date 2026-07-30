# Phase 4 – Authentication & User Registration

## 📌 Overview

In this phase, we implemented the complete User Registration module for the GramSeva platform.

The authentication module allows users to register securely by validating their information, hashing passwords before storing them, checking for duplicate email and phone numbers, and exposing a production-ready REST API through FastAPI.

This phase establishes the security foundation for the entire application.

---

# Objectives

- Build Authentication Module
- Create User Registration API
- Validate User Input
- Secure Password Storage
- Prevent Duplicate Registration
- Build Business Logic Layer
- Connect API with Database
- Test API using Swagger

---

# Folder Structure

```text
app/
│
├── api/
│   └── auth.py
│
├── core/
│   └── security.py
│
├── services/
│   └── auth_service.py
│
├── schemas/
│   ├── auth.py
│   └── token.py
│
├── models/
│   ├── base.py
│   └── user.py
│
├── db/
│   └── database.py
│
└── main.py
```

---

# Authentication Architecture

```text
Client

      │

      ▼

POST /auth/register

      │

      ▼

FastAPI Router

      │

      ▼

Authentication Service

      │

      ▼

Security Module

      │

      ▼

SQLAlchemy ORM

      │

      ▼

MySQL Database
```

---

# Features Implemented

## 1. Security Module

Implemented:

- Password Hashing
- Password Verification
- JWT Token Creation
- JWT Token Decoding
- OAuth2PasswordBearer

Functions created:

- hash_password()
- verify_password()
- create_access_token()
- decode_access_token()

---

## 2. Authentication Schemas

Created:

### UserRegister

Fields

- full_name
- email
- phone
- password
- role

Validation:

- Email validation
- Password minimum length
- Name length validation
- Phone validation

---

### UserLogin

Prepared for Login API.

---

### UserResponse

Returns only safe information.

Includes:

- id
- full_name
- email
- role

Does NOT expose:

- password
- phone

---

### Token

Prepared for JWT Authentication.

---

# Authentication Service

Business logic implemented inside

```text
app/services/auth_service.py
```

Responsibilities:

- Check duplicate email
- Check duplicate phone
- Hash password
- Save user
- Commit transaction
- Refresh object
- Return user

---

# API Endpoint

## Register User

```http
POST /auth/register
```

Request Body

```json
{
  "full_name": "Neeraj Sharma",
  "email": "neeraj@gmail.com",
  "phone": "9876543210",
  "password": "Admin@123",
  "role": "citizen"
}
```

Successful Response

```json
{
  "id": 1,
  "full_name": "Neeraj Sharma",
  "email": "neeraj@gmail.com",
  "role": "citizen"
}
```

Status Code

```
201 Created
```

---

# Validation Implemented

## Duplicate Email

If email already exists

Response

```
400 Bad Request
```

Message

```
Email already registered.
```

---

## Duplicate Phone

If phone already exists

Response

```
400 Bad Request
```

Message

```
Phone number already registered.
```

---

# Password Security

Passwords are never stored as plain text.

Before saving:

```text
Admin@123
```

Stored in database as:

```text
$2b$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

This uses bcrypt hashing through Passlib.

---

# Swagger Testing

Successfully verified:

✅ Register User

✅ User Validation

✅ Duplicate Email

✅ Duplicate Phone

✅ Response Model

✅ Status Codes

---

# Files Created

```text
app/core/security.py

app/schemas/auth.py

app/schemas/token.py

app/services/auth_service.py

app/api/auth.py
```

---

# Files Updated

```text
app/main.py

app/models/user.py

app/models/base.py

app/db/database.py
```

---

# Concepts Learned

- FastAPI Routing
- APIRouter
- Dependency Injection
- Depends()
- SQLAlchemy Session
- Service Layer Architecture
- Password Hashing
- JWT Fundamentals
- Pydantic Validation
- Response Models
- HTTP Status Codes
- Exception Handling
- Swagger Documentation

---

# Challenges Faced

## Issue 1

bcrypt compatibility issue.

Solution:

Downgraded bcrypt to compatible version.

---

## Issue 2

Schema and Database Model mismatch.

Phone field was missing.

Solution:

Updated UserRegister schema.

---

## Issue 3

Authentication router not visible in Swagger.

Solution:

- Added APIRouter
- Included router in main.py
- Restarted server

---

## Issue 4

Import error

```
cannot import router
```

Solution:

Completed auth.py implementation and verified imports.

---

# Lessons Learned

- Always verify each layer before moving forward.
- Never store plain-text passwords.
- Keep API, Service, and Database layers separate.
- Validate user input using Pydantic.
- Return only required fields to clients.
- Test every endpoint using Swagger.
- Debug by identifying the root cause instead of guessing.

---

# Production Best Practices

- Use Service Layer for business logic.
- Hash passwords before storing them.
- Never expose passwords in API responses.
- Return proper HTTP status codes.
- Use response models for data protection.
- Keep routers modular.
- Use Alembic for future database schema changes.

---

# Phase Completion Checklist

- [x] Security Module
- [x] Authentication Schemas
- [x] User Registration Service
- [x] Register API
- [x] Swagger Integration
- [x] Password Hashing
- [x] Duplicate Email Validation
- [x] Duplicate Phone Validation
- [x] End-to-End Testing

---

# Git Commands

```bash
git status
git add .
git commit -m "feat(auth): implement user registration module"
git push origin main
```

---

# Next Phase

Phase 5 – Login & JWT Authentication

Upcoming Features:

- Login API
- JWT Token Generation
- OAuth2 Authentication
- Protected APIs
- Current User API
- Role-Based Authorization
- Swagger Authorize Button
- JWT Token Verification