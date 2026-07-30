# 📘 Phase 2 - Project Setup & Backend Foundation

## 📌 Phase Information

**Project Name:** GramSeva – AI Powered Smart Village Governance Platform

**Phase:** 2

**Status:** ✅ Completed

---

# 🎯 Objective

The objective of this phase was to create a production-ready project structure and prepare the complete backend development environment.

Instead of writing business logic immediately, we first built a strong project foundation so that future development becomes easier, scalable, and maintainable.

---

# 🏗️ Project Folder Structure

A professional project structure was created.

```text
GramSeva/

├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── alembic/
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── .env
│   └── venv/
│
├── frontend/
├── database/
├── docs/
├── tests/
├── assets/
├── screenshots/
├── README.md
└── .gitignore
```

---

# ⚙️ Development Environment

The following software was installed and configured.

- Python
- Visual Studio Code
- Git
- GitHub
- MySQL Workbench
- MySQL Server

---

# 🐍 Virtual Environment

A dedicated Python Virtual Environment was created.

Purpose:

- Isolate project dependencies
- Avoid package conflicts
- Maintain consistent development environment

Command used:

```bash
python -m venv venv
```

---

# 📦 Python Packages Installed

The following packages were installed.

- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- PyMySQL
- Pydantic Settings
- Python Dotenv

---

# ⚡ FastAPI Initialization

FastAPI backend was successfully initialized.

Main application file:

```text
backend/app/main.py
```

The application successfully started on:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

# 🔐 Environment Variables

Sensitive information was moved into the `.env` file.

Stored values include:

- Database Host
- Database Port
- Database Name
- Database Username
- Database Password
- Secret Key
- JWT Algorithm
- Token Expiry Time

Purpose:

- Better security
- Easy deployment
- No hardcoded credentials

---

# ⚙️ Configuration Module

A centralized configuration module was created.

File:

```
app/core/config.py
```

Responsibilities:

- Read environment variables
- Validate configuration
- Provide settings throughout the application

---

# 🗄️ Database Connectivity

A reusable database connection module was created.

File:

```
app/db/database.py
```

Responsibilities:

- Create SQLAlchemy Engine
- Manage Sessions
- Create Declarative Base
- Provide Dependency Injection

---

# 🌐 API Testing

FastAPI server was tested successfully.

Custom APIs were created for testing.

Examples:

- Root API
- Database Connection API

Database connectivity was successfully verified.

---

# 📂 Files Created

```
backend/

app/

main.py

core/
config.py

db/
database.py

.env

requirements.txt

alembic.ini
```

---

# 🚀 Industry Best Practices Applied

The following professional practices were followed.

- Layered Project Structure
- Environment Variables
- Virtual Environment
- Modular Architecture
- Secure Configuration
- Dependency Management
- Separation of Concerns
- Production Folder Structure

---

# 🎤 Presentation Explanation

"In this phase, we prepared the complete backend development environment. We created a production-ready folder structure, configured FastAPI, installed required libraries, connected the project with MySQL, and securely stored configuration values using environment variables. This setup provides a strong and scalable foundation for future development."

---

# 💬 Interview Questions

1. What is FastAPI?

2. Why did you choose FastAPI?

3. What is a Virtual Environment?

4. Why do we use `.env` files?

5. What is Uvicorn?

6. Why is modular architecture important?

7. What is Dependency Injection?

8. Why should credentials never be hardcoded?

9. Explain the folder structure of your project.

10. Why did you separate backend and frontend?

---

# 📚 Lessons Learned

During this phase, we learned:

- FastAPI project initialization
- Backend architecture
- Python Virtual Environment
- Environment Variables
- Secure Configuration
- Dependency Management
- Modular Project Structure
- Database Connectivity Basics

---

# ⚠️ Challenges Faced

Several real-world challenges were encountered.

- MySQL installation issues
- Database connection failures
- Environment variable loading issues
- Alembic configuration issues
- Password encoding (`@`) issue
- Migration setup errors
- Backend folder restructuring

---

# ✅ How We Solved Them

The problems were solved using an industry-standard debugging approach.

- Reinstalled MySQL cleanly
- Reset root password
- Verified environment variables
- Tested database connectivity independently
- Debugged SQLAlchemy configuration
- Fixed Alembic configuration
- Reorganized backend architecture
- Verified each layer before moving forward

Instead of guessing, each issue was isolated and tested step by step until the root cause was identified.

---

# 🎯 Next Phase Goals

In the next phase we will build the complete database layer.

Upcoming tasks:

- SQLAlchemy Models
- Base Model
- User Model
- Database Relationships
- Alembic Migrations
- Database Version Control

---

# 📝 Phase Summary

### ✅ Completed

- Production folder structure
- FastAPI initialization
- Virtual Environment
- Dependency installation
- Environment configuration
- Database connection
- Configuration module
- SQLAlchemy setup foundation
- Secure project architecture

---

# 📊 Phase Completion

**Status:** ✅ Completed Successfully

**Next Phase:** Database Design & ORM