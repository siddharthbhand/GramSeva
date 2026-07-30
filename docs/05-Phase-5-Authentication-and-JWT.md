# Phase 5 - Authentication & JWT

---

# Overview

In this phase, the authentication system for the GramSeva project was implemented.

The goal of this phase was to securely authenticate users, generate JWT tokens after successful login, and protect APIs so that only authenticated users can access them.

Authentication is one of the most important modules of the project because every other module depends on user identity and permissions.

---

# Objectives

The objectives of this phase were:

- Implement secure user login
- Verify user credentials
- Generate JWT Access Token
- Protect private APIs
- Get currently logged-in user
- Follow FastAPI OAuth2 Authentication standard
- Build a production-ready authentication system

---

# Authentication Flow

```
User
   │
   ▼
Login
   │
   ▼
Verify Email
   │
   ▼
Verify Password
   │
   ▼
Generate JWT Token
   │
   ▼
Return Access Token
   │
   ▼
Store Token
   │
   ▼
Protected API Access
```

---

# Folder Structure

```
app/

├── api/
│      auth.py

├── core/
│      security.py

├── dependencies/
│      auth.py

├── schemas/
│      auth.py
│      token.py

├── services/
│      auth_service.py
```

---

# Files Created / Updated

## 1. app/core/security.py

Responsibilities

- Password Hashing
- Password Verification
- JWT Token Generation
- JWT Token Verification
- OAuth2 Configuration

Implemented Functions

- hash_password()
- verify_password()
- create_access_token()
- decode_access_token()

---

## 2. app/services/auth_service.py

Responsibilities

- Register User
- Login User
- Verify Credentials
- Generate JWT Token

Implemented Methods

- register_user()
- login_user()

---

## 3. app/api/auth.py

Implemented APIs

POST /auth/register

POST /auth/login

GET /auth/me

---

## 4. app/dependencies/auth.py

Responsibilities

- Verify JWT Token
- Decode Token
- Get Current Logged-in User
- Protect Private APIs

---

## 5. app/schemas/token.py

Created Token Schema

Contains

- access_token
- token_type

---

# APIs Implemented

## Register

Endpoint

```
POST /auth/register
```

Purpose

Register a new user.

---

## Login

Endpoint

```
POST /auth/login
```

Purpose

Authenticate user and generate JWT token.

Request Type

OAuth2PasswordRequestForm

Required Fields

- username (Email)
- password

Response

```json
{
    "access_token": "...",
    "token_type": "bearer"
}
```

---

## Current User

Endpoint

```
GET /auth/me
```

Purpose

Returns currently logged-in user information.

Response

```json
{
    "id": 1,
    "full_name": "Neeraj",
    "email": "neeraj@gmail.com",
    "role": "citizen"
}
```

---

# JWT Authentication

JWT (JSON Web Token) is used for authentication.

After successful login:

- JWT token is generated.
- Token is returned to the client.
- Client sends the token with every protected request.
- Server validates the token.
- If valid, access is granted.

---

# Password Security

Passwords are never stored in plain text.

Before saving:

```
Plain Password
        │
        ▼
Password Hashing
        │
        ▼
Database
```

During Login

```
Entered Password
        │
        ▼
Verify Hash
        │
        ▼
Login Success
```

bcrypt hashing algorithm is used for password security.

---

# OAuth2 Authentication

The project uses FastAPI's OAuth2PasswordBearer.

Benefits

- Industry Standard
- Swagger Authorization Support
- Secure Token Authentication
- Production Ready

---

# Protected Routes

Protected APIs require a valid JWT token.

Implemented Protected API

```
GET /auth/me
```

Only authenticated users can access this endpoint.

---

# Authentication Workflow

```
Register User

↓

Login

↓

Generate JWT

↓

Authorize

↓

Access Protected APIs

↓

Current User
```

---

# Swagger Testing

Successfully Tested

- Register User
- Login User
- JWT Token Generation
- Authorize Button
- Protected Route
- Current User API

All APIs returned successful responses.

---

# Challenges Faced

## Issue 1

Swagger Authorization was not working.

Reason

Login API initially accepted JSON request body.

Solution

Converted Login API to OAuth2PasswordRequestForm.

---

## Issue 2

Protected API returned

```
401 Unauthorized
```

Reason

JWT token was not being sent.

Solution

Used Swagger Authorize feature to send Bearer Token automatically.

---

## Issue 3

bcrypt compatibility issue.

Reason

bcrypt version conflict.

Solution

Installed bcrypt 4.0.1.

---

# Concepts Learned

- Authentication
- Authorization
- JWT
- OAuth2
- Password Hashing
- Protected APIs
- Dependency Injection
- Service Layer
- FastAPI Security
- Token Validation

---

# Best Practices Followed

- Layered Architecture
- Service Layer Pattern
- JWT Authentication
- Password Hashing
- OAuth2 Standard
- Pydantic Validation
- Clean Folder Structure
- Secure APIs
- Proper HTTP Status Codes

---

# Phase Completion Checklist

- User Registration
- Login
- JWT Token
- Password Hashing
- OAuth2 Authentication
- Protected Routes
- Current User API
- Swagger Testing
- Error Handling

Status

```
Completed
```

---

# Learning Outcome

After completing this phase, the project now has a complete production-ready authentication system.

Users can:

- Register
- Login
- Receive JWT Token
- Access Protected APIs
- Retrieve Current User Information

The authentication module now serves as the foundation for all future modules such as User Management, Complaint Management, Notices, Gram Sabha, Certificates, and other protected features.

---

# Next Phase

Phase 6

User Management Module

Features

- View Users
- Update Users
- Delete Users
- Activate/Deactivate Users
- Role Management