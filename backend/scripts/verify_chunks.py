"""
Verification script for ingested content.
Checks chunk count, performs sample queries, and validates collection health.
"""

import sys
import asyncio
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.qdrant_service import qdrant_service
from services.openai_service import openai_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def verify_collection():
    """Verify Qdrant collection health and content."""
    logger.info("=" * 60)
    logger.info("Verifying Qdrant Collection")
    logger.info("=" * 60)

    try:
        # Get collection info
        info = qdrant_service.get_collection_info()
        logger.info(f"✅ Collection exists: {qdrant_service.collection_name}")
        logger.info(f"   Vectors count: {info['vectors_count']}")
        logger.info(f"   Points count: {info['points_count']}")
        logger.info(f"   Status: {info['status']}")

        if info['vectors_count'] == 0:
            logger.warning("⚠️  Collection is empty! Run ingestion script first.")
            return False

        # Sample queries
        sample_queries = [
            "What is ROS 2?",
            "How do I create a custom message?",
            "What is URDF?",
            "What are the prerequisites?"
        ]

        logger.info("\n" + "=" * 60)
        logger.info("Running Sample Queries")
        logger.info("=" * 60)

        for query_text in sample_queries:
            logger.info(f"\nQuery: '{query_text}'")

            # Generate embedding
            embedding = await openai_service.embed_text(query_text)

            # Search
            results = await qdrant_service.search(
                query_vector=embedding,
                limit=3,
                score_threshold=0.5
            )

            if results:
                logger.info(f"   Found {len(results)} results:")
                for i, result in enumerate(results, 1):
                    logger.info(f"   {i}. Module {result['module_number']}, "
                              f"Chapter {result['chapter_number']} "
                              f"(score: {result['score']:.3f})")
                    logger.info(f"      {result['section_title']}")
                    logger.info(f"      {result['content_text'][:100]}...")
            else:
                logger.warning(f"   ⚠️  No results found")

        logger.info("\n" + "=" * 60)
        logger.info("✅ Verification Complete")
        logger.info("=" * 60)

        return True

    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(verify_collection())
    sys.exit(0 if success else 1)
