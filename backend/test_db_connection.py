"""
Test database connection to verify DATABASE_URL is correct.
"""

import sys
from config import settings

print("Testing database connection...")
# Mask password in output
db_url_display = settings.database_url
if "@" in db_url_display:
    parts = db_url_display.split("@")
    if len(parts) == 2:
        user_pass = parts[0].split("://")[1] if "://" in parts[0] else parts[0]
        if ":" in user_pass:
            user = user_pass.split(":")[0]
            db_url_display = db_url_display.replace(user_pass, f"{user}:***")
print(f"Database URL: {db_url_display[:80]}..." if len(db_url_display) > 80 else f"Database URL: {db_url_display}")

# Check if pointing to localhost
if "localhost" in settings.database_url or "127.0.0.1" in settings.database_url:
    print("ℹ️  Using local PostgreSQL database (this is fine!)")
    
    # Check for URL encoding issues
    if "%%" in settings.database_url or "%40" in settings.database_url:
        print("\n⚠️  WARNING: Password appears to be URL-encoded!")
        print("   If your password contains special characters, they may need to be URL-encoded.")
        print("   Common encodings:")
        print("   - @ becomes %40")
        print("   - # becomes %23")
        print("   - % becomes %25")
        print("   - Space becomes %20")
else:
    print("ℹ️  Using remote database")

# Try to connect
print("\nAttempting to connect...")
try:
    from models.database import engine
    from sqlalchemy import text
    with engine.connect() as conn:
        print("✅ Database connection successful!")
        
        # Get PostgreSQL version
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"   PostgreSQL version: {version[:60]}...")
        
        # Check if tables exist
        print("\nChecking database tables...")
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        tables = [row[0] for row in result.fetchall()]
        if tables:
            print(f"   Found {len(tables)} table(s): {', '.join(tables)}")
            required_tables = ['chat_sessions', 'user_queries', 'chat_responses', 'user_feedback']
            missing = [t for t in required_tables if t not in tables]
            if missing:
                print(f"   ⚠️  Missing tables: {', '.join(missing)}")
                print("   Run: alembic upgrade head")
            else:
                print("   ✅ All required tables exist")
        else:
            print("   ⚠️  No tables found. Run: alembic upgrade head")
            
except Exception as e:
    error_msg = str(e)
    print(f"\n❌ Database connection failed!")
    print(f"   Error: {error_msg}")
    
    print("\nTroubleshooting steps:")
    if "password authentication failed" in error_msg.lower():
        print("1. ❌ Password authentication failed")
        print("   - Check your password in .env file")
        print("   - If password contains special characters, try URL-encoding them:")
        print("     @ → %40, # → %23, % → %25, space → %20")
        print("   - Or wrap the entire connection string in quotes if it has spaces")
    elif "could not connect" in error_msg.lower() or "connection refused" in error_msg.lower():
        print("1. ❌ Cannot connect to database server")
        print("   - Is PostgreSQL running? Check: pg_ctl status")
        print("   - Is it listening on port 5432?")
        print("   - Check Windows Services for 'postgresql' service")
    elif "database" in error_msg.lower() and "does not exist" in error_msg.lower():
        print("1. ❌ Database does not exist")
        print("   - Create the database: CREATE DATABASE your_db_name;")
    else:
        print("1. Check DATABASE_URL format in .env")
        print("2. Verify PostgreSQL is running")
        print("3. Check database credentials")
        print("4. Ensure database exists")
    
    print("\nExample .env format for local PostgreSQL:")
    print('DATABASE_URL=postgresql://postgres:your_password@localhost:5432/your_database')
    print("\nIf password has special characters, URL-encode them:")
    print('DATABASE_URL=postgresql://postgres:pass%40word@localhost:5432/dbname')
    
    sys.exit(1)

