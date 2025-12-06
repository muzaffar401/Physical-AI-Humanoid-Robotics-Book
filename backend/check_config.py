"""
Quick script to check if environment variables are loaded correctly.
Run this to diagnose configuration issues.
"""

import os
from pathlib import Path

print("=" * 60)
print("Configuration Check")
print("=" * 60)

# Check if .env file exists
env_path = Path(__file__).parent / ".env"
print(f"\n1. .env file exists: {env_path.exists()}")
if env_path.exists():
    print(f"   Location: {env_path}")
    print(f"   Size: {env_path.stat().st_size} bytes")
else:
    print("   ❌ ERROR: .env file not found!")
    print(f"   Expected location: {env_path}")

# Check environment variables
print("\n2. Environment Variables:")
required_vars = [
    "OPENAI_API_KEY",
    "QDRANT_URL",
    "QDRANT_API_KEY",
    "DATABASE_URL",
]

for var in required_vars:
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        if "KEY" in var or "PASSWORD" in var or var == "DATABASE_URL":
            if len(value) > 20:
                masked = value[:10] + "..." + value[-10:]
            else:
                masked = "***" + value[-5:] if len(value) > 5 else "***"
            print(f"   ✅ {var}: {masked}")
        else:
            print(f"   ✅ {var}: {value}")
    else:
        print(f"   ❌ {var}: NOT SET")

# Try to load config
print("\n3. Loading config.py:")
try:
    from config import settings
    print("   ✅ Config loaded successfully")
    print(f"   Database URL configured: {settings.database_url[:30]}..." if len(settings.database_url) > 30 else f"   Database URL: {settings.database_url}")
    
    # Check if it's pointing to localhost
    if "localhost" in settings.database_url or "127.0.0.1" in settings.database_url:
        print("   ⚠️  WARNING: DATABASE_URL points to localhost!")
        print("   This should point to your Neon Postgres database.")
        print("   Expected format: postgresql://user:pass@host-pooler.neon.tech/dbname?sslmode=require")
except Exception as e:
    print(f"   ❌ Error loading config: {e}")

print("\n" + "=" * 60)
print("If DATABASE_URL is not set or points to localhost:")
print("1. Create/update backend/.env file")
print("2. Add: DATABASE_URL=postgresql://user:pass@host-pooler.neon.tech/dbname?sslmode=require")
print("3. Use the POOLED connection string from Neon dashboard")
print("=" * 60)

