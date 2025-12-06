"""Quick API test to diagnose internal server errors."""
import asyncio
import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')

async def test_embedding_service():
    """Test embedding service initialization."""
    print("1. Testing Embedding Service...")
    try:
        from services.embedding_service import embedding_service
        print("   ✓ Embedding service initialized successfully")
        print(f"   Model info: {embedding_service.get_model_info()}")

        # Test embedding
        test_text = "What is ROS 2?"
        embedding = embedding_service.embed_text(test_text)
        print(f"   ✓ Generated embedding with {len(embedding)} dimensions")
        return True
    except Exception as e:
        print(f"   ✗ Embedding service failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_qdrant_service():
    """Test Qdrant connection."""
    print("\n2. Testing Qdrant Service...")
    try:
        from services.qdrant_service import qdrant_service
        print("   ✓ Qdrant service initialized")

        # Test collection info
        info = qdrant_service.get_collection_info()
        print(f"   ✓ Collection info: {info}")
        return True
    except Exception as e:
        print(f"   ✗ Qdrant service failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_database_service():
    """Test database connection."""
    print("\n3. Testing Database Service...")
    try:
        from models.database import SessionLocal, engine
        from services.database_service import database_service

        # Test connection
        with SessionLocal() as db:
            # Simple query to test connection
            from models.database import ChatSession
            count = db.query(ChatSession).count()
            print(f"   ✓ Database connected - {count} sessions found")
        return True
    except Exception as e:
        print(f"   ✗ Database service failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_openai_service():
    """Test OpenAI service."""
    print("\n4. Testing OpenAI Service...")
    try:
        from services.openai_service import openai_service
        print("   ✓ OpenAI service initialized")

        # Test simple generation
        messages = [{"role": "user", "content": "Say hello"}]
        result = await openai_service.generate_response(messages)
        print(f"   ✓ Generated response: {result['response_text'][:50]}...")
        return True
    except Exception as e:
        print(f"   ✗ OpenAI service failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_rag_service():
    """Test RAG service end-to-end."""
    print("\n5. Testing RAG Service...")
    try:
        from services.rag_service import rag_service
        print("   ✓ RAG service initialized")

        # Test generate_answer
        result = await rag_service.generate_answer(
            query_text="What is ROS 2?",
            mode="full_book"
        )
        print(f"   ✓ Generated answer in {result['response_time_ms']}ms")
        print(f"   ✓ Found {len(result['source_chunks'])} source chunks")
        print(f"   Response: {result['response_text'][:100]}...")
        return True
    except Exception as e:
        print(f"   ✗ RAG service failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    print("=" * 60)
    print("RAG Chatbot API - Service Tests")
    print("=" * 60)

    results = {
        "Embedding Service": await test_embedding_service(),
        "Qdrant Service": await test_qdrant_service(),
        "Database Service": await test_database_service(),
        "OpenAI Service": await test_openai_service(),
        "RAG Service": await test_rag_service(),
    }

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for service, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {service}")

    all_passed = all(results.values())
    print("\n" + ("All tests passed! 🎉" if all_passed else "Some tests failed ❌"))
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
