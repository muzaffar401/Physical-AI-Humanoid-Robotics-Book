# Fix Local PostgreSQL Connection

## Current Issue
Password authentication is failing. Your password appears to be incorrectly URL-encoded.

## Solution

### Option 1: Fix Password Encoding (Recommended)

If your password is `Commtel@123`, update your `.env` file:

**Current (incorrect):**
```
DATABASE_URL=postgresql://postgres:Commtel%%40123@localhost:5432/rag_chatbot
```

**Correct format:**
```
DATABASE_URL=postgresql://postgres:Commtel%40123@localhost:5432/rag_chatbot
```

Note: `@` should be encoded as `%40` (single encoding), not `%%40` (double encoding).

### Option 2: Use Plain Password (If no special chars)

If your password doesn't have special characters, use it directly:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/rag_chatbot
```

### Option 3: Verify Your Actual Password

1. Open pgAdmin or psql
2. Try connecting with your password
3. If it works there, use the same password in `.env`

### Special Character Encoding Reference

| Character | Encoding |
|-----------|----------|
| `@` | `%40` |
| `#` | `%23` |
| `%` | `%25` |
| Space | `%20` |
| `:` | `%3A` |
| `/` | `%2F` |
| `?` | `%3F` |

### Verify Database Exists

Make sure the database `rag_chatbot` exists:

```sql
-- Connect to PostgreSQL
psql -U postgres

-- List databases
\l

-- If rag_chatbot doesn't exist, create it
CREATE DATABASE rag_chatbot;
```

### After Fixing

1. Update `.env` file with correct password
2. Test connection: `python test_db_connection.py`
3. If successful, run migrations: `alembic upgrade head`
4. Restart backend: `uvicorn main:app --reload`

