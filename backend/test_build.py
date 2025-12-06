#!/usr/bin/env python3
"""
Build verification script - tests all critical imports
"""

print("Testing critical imports...")

try:
    print("[OK] Testing FastAPI...")
    from fastapi import FastAPI

    print("[OK] Testing uvicorn...")
    import uvicorn

    print("[OK] Testing psycopg2 (PostgreSQL driver)...")
    import psycopg2

    print("[OK] Testing SQLAlchemy...")
    from sqlalchemy import create_engine

    print("[OK] Testing OpenAI...")
    import openai

    print("[OK] Testing sentence-transformers...")
    from sentence_transformers import SentenceTransformer

    print("[OK] Testing torch...")
    import torch

    print("[OK] Testing qdrant-client...")
    from qdrant_client import QdrantClient

    print("[OK] Testing pydantic...")
    from pydantic import BaseModel

    print("[OK] Testing alembic...")
    import alembic

    print("\n[SUCCESS] All critical imports successful!")
    print(f"   Python: {__import__('sys').version}")
    print(f"   FastAPI: {FastAPI.__version__ if hasattr(FastAPI, '__version__') else 'installed'}")
    print(f"   PyTorch: {torch.__version__}")
    print(f"   SQLAlchemy: {__import__('sqlalchemy').__version__}")

except ImportError as e:
    print(f"\n[ERROR] Import failed: {e}")
    exit(1)

print("\n[SUCCESS] Build verification complete!")
