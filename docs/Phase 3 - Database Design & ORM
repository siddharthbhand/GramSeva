# 📘 Phase 3 - Database Design & ORM

## 📌 Phase Information

**Project Name:** GramSeva – AI Powered Smart Village Governance Platform

**Phase:** 3

**Status:** ✅ Completed

---

# 🎯 Objective

The objective of this phase was to design a scalable database architecture, establish communication between FastAPI and MySQL using SQLAlchemy ORM, and implement database version control using Alembic.

A well-designed database is the backbone of every software application. Therefore, before implementing APIs, we created a strong and maintainable database foundation.

---

# 🗄️ Database Selection

We selected **MySQL** as the primary relational database because it is:

- Open Source
- Reliable
- Scalable
- Easy to Maintain
- Widely Used in Industry

Database Name:

```text
gramseva
```

---

# 🏗️ ORM (Object Relational Mapping)

Instead of writing raw SQL queries, we used **SQLAlchemy ORM**.

ORM allows developers to interact with database tables using Python classes.

Example:

Instead of writing SQL,

```sql
SELECT * FROM users;
```

We can simply write Python code using SQLAlchemy models.

Benefits:

- Cleaner Code
- Better Readability
- Reusable Models
- Database Independence
- Easier Maintenance

---

# ⚙️ SQLAlchemy Configuration

A reusable SQLAlchemy engine was configured.

Responsibilities:

- Create Database Engine
- Manage Database Sessions
- Handle Connections
- Provide Dependency Injection

File:

```
backend/app/db/database.py
```

---

# 🧱 Base Model

A reusable Base Model was created.

Purpose:

- Reduce duplicate code
- Maintain consistency
- Share common fields across all tables

Common fields:

- id
- created_at
- updated_at

Every future model in the project will inherit from this Base Model.

---

# 👤 User Model

The first database model created was the **User Model**.

The model represents all users of the system, including:

- Citizens
- Officers
- Admins
- Higher Authorities
- Super Admins

This table will act as the foundation for the authentication system in the next phase.

---

# 🔄 Alembic Migration

Alembic was configured for database version control.

Migration provides a safe way to create and update database tables without manually writing SQL scripts.

Migration generated:

```bash
python -m alembic revision --autogenerate -m "Initial Migration"
```

Migration applied successfully:

```bash
python -m alembic upgrade head
```

Result:

```
INFO Running upgrade -> Initial Migration
```

---

# 📂 Files Created

```
backend/

app/

db/
database.py

models/
base.py
user.py

core/
config.py

alembic/

versions/

alembic.ini
```

---

# 🔐 Environment Configuration

Database credentials were securely stored inside the `.env` file.

Example:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=gramseva
DB_USER=root
DB_PASSWORD=********

SECRET_KEY=********
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

This approach improves security and simplifies deployment.

---

# 🚀 Industry Best Practices Applied

The following best practices were followed:

- Layered Architecture
- SQLAlchemy ORM
- Reusable Database Session
- Base Model Inheritance
- Environment Variables
- Database Version Control
- Modular Code Structure
- Separation of Concerns

---

# 🐞 Challenges Faced

During this phase, several real-world issues were encountered.

### 1. Database Connection Failed

Initially, FastAPI was unable to connect with MySQL.

---

### 2. Password Encoding Issue

The database password contained the `@` character.

This caused SQLAlchemy to incorrectly parse the database URL.

---

### 3. Alembic Configuration Issues

Alembic was unable to detect models correctly during migration.

---

### 4. Migration Errors

Initial migrations failed due to incorrect database configuration.

---

### 5. SQLAlchemy Engine Configuration

Engine initialization required proper configuration for successful migrations.

---

# ✅ How We Solved Them

Each issue was solved using a systematic debugging approach.

- Verified MySQL service status
- Confirmed database credentials
- Updated the database password to avoid URL parsing issues
- Correctly configured SQLAlchemy engine
- Updated Alembic configuration
- Imported metadata properly
- Regenerated migration
- Successfully applied migration using Alembic

Instead of applying random fixes, every issue was analyzed and resolved step by step.

---

# 🧪 Testing Performed

The following validations were completed.

✅ Database connection successful

✅ SQLAlchemy engine working

✅ Sessions created successfully

✅ User model detected

✅ Alembic migration generated

✅ Migration applied successfully

✅ Database schema created

---

# 📚 Lessons Learned

During this phase, we learned:

- Database Design
- SQLAlchemy ORM
- SQLAlchemy Engine
- Session Management
- Declarative Base
- Model Creation
- Alembic
- Database Version Control
- Database Migrations
- Professional Debugging Techniques

---

# 🎤 Presentation Explanation

"In this phase, we designed the complete database architecture for GramSeva. We connected FastAPI with MySQL using SQLAlchemy ORM and implemented Alembic for database version control. We also created reusable database components such as the SQLAlchemy engine, Base Model, and User Model. Finally, we generated and applied the initial migration successfully."

---

# 💬 Interview Questions

1. What is SQLAlchemy?

2. What is ORM?

3. Why use ORM instead of raw SQL?

4. What is Alembic?

5. What is Database Migration?

6. Why do we use Base Models?

7. What is Session Management?

8. What is SQLAlchemy Engine?

9. Why are migrations important?

10. Explain your database architecture.

11. What debugging challenges did you face?

12. How did you solve the Alembic migration issue?

---

# 📝 Git History

## Commit 1

Create SQLAlchemy database configuration

---

## Commit 2

Add Base Model and User Model

---

## Commit 3

Configure Alembic migrations

---

## Commit 4

Generate Initial Migration

---

## Commit 5

Apply database migration successfully

---

## Commit 6

Fix SQLAlchemy and Alembic configuration issues

---

## Commit 7

Complete Phase 3 Database Foundation

---

# 🎯 Next Phase Goals

The next phase focuses on building a secure authentication system.

Upcoming tasks:

- JWT Authentication
- Password Hashing
- User Registration
- Login API
- Protected Routes
- Dependency Injection
- Role-Based Access Control
- Swagger API Testing

---

# 📝 Phase Summary

### ✅ Completed

- MySQL Database Created
- SQLAlchemy Configured
- Database Engine Created
- Session Management Implemented
- Base Model Created
- User Model Created
- Alembic Configured
- Initial Migration Generated
- Migration Applied Successfully
- Database Connected with FastAPI

---

# 📊 Phase Completion

**Status:** ✅ Completed Successfully

**Next Phase:** Authentication & User Management