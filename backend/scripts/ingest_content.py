"""
Content ingestion script for RAG chatbot.
Parses markdown files, chunks content, generates embeddings, and uploads to Qdrant.
"""

import os
import sys
import asyncio
import logging
import argparse
import uuid
from pathlib import Path
from typing import List, Dict, Any
import yaml
from markdown_it import MarkdownIt
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Add parent directory to path to import services
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.qdrant_service import qdrant_service
from services.embedding_service import EmbeddingService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ContentIngester:
    """Handles content ingestion from markdown files to Qdrant."""

    def __init__(self, base_url: str = "https://muzaffar401.github.io/Physical-AI-Humanoid-Robotics-Book"):
        """
        Initialize content ingester.

        Args:
            base_url: Base URL for the published book
        """
        self.base_url = base_url
        self.md_parser = MarkdownIt()
        self.embedding_service = EmbeddingService()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # ~750 tokens
            chunk_overlap=100,
            separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
            length_function=len,
            keep_separator=True
        )

    def extract_frontmatter(self, content: str) -> tuple[Dict[str, Any], str]:
        """
        Extract YAML frontmatter from markdown content.

        Args:
            content: Markdown file content

        Returns:
            Tuple of (metadata dict, content without frontmatter)
        """
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                    content_without_frontmatter = parts[2].strip()
                    return metadata or {}, content_without_frontmatter
                except yaml.YAMLError as e:
                    logger.warning(f"Error parsing YAML frontmatter: {e}")

        return {}, content

    def parse_file_path(self, file_path: Path, docs_dir: Path) -> Dict[str, Any]:
        """
        Extract metadata from file path.

        Args:
            file_path: Path to markdown file
            docs_dir: Base docs directory

        Returns:
            Dict with module_number, chapter_number, file_path, public_url
        """
        relative_path = file_path.relative_to(docs_dir)
        path_parts = relative_path.parts

        metadata = {
            "file_path": str(relative_path),
            "module_number": None,
            "chapter_number": None,
            "section_title": file_path.stem.replace("-", " ").title()
        }

        # Try to extract module and chapter from path (e.g., module-1/chapter-1-2-pubsub.md)
        for part in path_parts:
            if part.startswith("module-"):
                try:
                    metadata["module_number"] = int(part.split("-")[1])
                except (IndexError, ValueError):
                    pass

            if file_path.stem.startswith("chapter-"):
                try:
                    chapter_parts = file_path.stem.split("-")
                    if len(chapter_parts) >= 3:
                        metadata["chapter_number"] = int(chapter_parts[1])
                except (IndexError, ValueError):
                    pass
            elif file_path.stem in ("index", "intro"):
                # Assign chapter 0 to index/intro files
                metadata["chapter_number"] = 0

        # Construct public URL
        url_path = str(relative_path).replace("\\", "/").replace(".md", "").replace(".mdx", "")
        metadata["public_url"] = f"{self.base_url}/docs/{url_path}"

        return metadata

    def chunk_content(self, content: str) -> List[str]:
        """
        Split content into chunks.

        Args:
            content: Markdown content

        Returns:
            List of text chunks
        """
        # Remove HTML comments and empty lines
        lines = []
        for line in content.split("\n"):
            if not line.strip().startswith("<!--") and not line.strip().endswith("-->"):
                lines.append(line)

        cleaned_content = "\n".join(lines)

        # Split into chunks
        chunks = self.text_splitter.split_text(cleaned_content)
        logger.debug(f"Split content into {len(chunks)} chunks")
        return chunks

    async def process_file(self, file_path: Path, docs_dir: Path) -> List[Dict[str, Any]]:
        """
        Process a single markdown file.

        Args:
            file_path: Path to markdown file
            docs_dir: Base docs directory

        Returns:
            List of chunk dicts with metadata and content
        """
        try:
            logger.info(f"Processing: {file_path.name}")

            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract frontmatter
            frontmatter, content = self.extract_frontmatter(content)

            # Extract path metadata
            path_metadata = self.parse_file_path(file_path, docs_dir)

            # Override with frontmatter if available
            metadata = {**path_metadata, **frontmatter}

            # Chunk content
            chunks = self.chunk_content(content)

            # Create chunk objects
            chunk_objects = []
            for i, chunk_text in enumerate(chunks):
                chunk_id = str(uuid.uuid4())
                chunk_obj = {
                    "chunk_id": chunk_id,
                    "content_text": chunk_text.strip(),
                    "module_number": metadata.get("module_number"),
                    "chapter_number": metadata.get("chapter_number"),
                    "section_title": metadata.get("section_title", ""),
                    "file_path": metadata["file_path"],
                    "public_url": metadata["public_url"],
                    "token_count": len(chunk_text.split()),  # Rough estimate
                    "chunk_index": i
                }
                chunk_objects.append(chunk_obj)

            logger.info(f"Created {len(chunk_objects)} chunks from {file_path.name}")
            return chunk_objects

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return []

    async def ingest_directory(self, docs_dir: Path, batch_size: int = 50) -> int:
        """
        Ingest all markdown files from a directory.

        Args:
            docs_dir: Directory containing markdown files
            batch_size: Number of chunks to process per batch

        Returns:
            Total number of chunks ingested
        """
        # Find all markdown files
        md_files = list(docs_dir.rglob("*.md")) + list(docs_dir.rglob("*.mdx"))
        logger.info(f"Found {len(md_files)} markdown files")

        if not md_files:
            logger.warning(f"No markdown files found in {docs_dir}")
            return 0

        # Process files
        all_chunks = []
        for file_path in md_files:
            chunks = await self.process_file(file_path, docs_dir)
            all_chunks.extend(chunks)

        logger.info(f"Total chunks created: {len(all_chunks)}")

        if not all_chunks:
            logger.warning("No chunks to ingest")
            return 0

        # Generate embeddings in batches using local sentence-transformers
        logger.info("Generating embeddings using local model (BAAI/bge-base-en-v1.5)...")
        chunk_texts = [chunk["content_text"] for chunk in all_chunks]
        embeddings = self.embedding_service.embed_batch(chunk_texts)

        logger.info(f"Generated {len(embeddings)} embeddings (768-dim)")

        # Prepare points for Qdrant
        points = []
        for chunk, embedding in zip(all_chunks, embeddings):
            point = {
                "chunk_id": chunk["chunk_id"],
                "embedding": embedding,
                "payload": {
                    "chunk_id": chunk["chunk_id"],
                    "content_text": chunk["content_text"],
                    "module_number": chunk["module_number"],
                    "chapter_number": chunk["chapter_number"],
                    "section_title": chunk["section_title"],
                    "file_path": chunk["file_path"],
                    "public_url": chunk["public_url"],
                    "token_count": chunk["token_count"],
                    "chunk_index": chunk["chunk_index"]
                }
            }
            points.append(point)

        # Upsert to Qdrant in batches
        logger.info("Uploading to Qdrant...")
        total_uploaded = 0

        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            count = await qdrant_service.upsert_batch(batch)
            total_uploaded += count
            logger.info(f"Uploaded batch {i // batch_size + 1}: {count} chunks")

        logger.info(f"✅ Successfully ingested {total_uploaded} chunks")
        return total_uploaded


async def main():
    """Main entry point for ingestion script."""
    parser = argparse.ArgumentParser(description="Ingest markdown content into Qdrant")
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Path to docs directory containing markdown files"
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default="https://muzaffar401.github.io/Physical-AI-Humanoid-Robotics-Book",
        help="Base URL for the published book"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Batch size for embedding generation and upload"
    )
    parser.add_argument(
        "--create-collection",
        action="store_true",
        help="Create Qdrant collection if it doesn't exist"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Delete existing collection and recreate (WARNING: destructive)"
    )

    args = parser.parse_args()

    # Validate source directory
    docs_dir = Path(args.source)
    if not docs_dir.exists():
        logger.error(f"Source directory not found: {docs_dir}")
        sys.exit(1)

    # Create collection if needed
    if args.force:
        logger.warning("⚠️  Force mode: deleting existing collection")
        try:
            qdrant_service.delete_collection()
        except Exception as e:
            logger.warning(f"Could not delete collection: {e}")

    if args.create_collection or args.force:
        logger.info("Creating Qdrant collection...")
        qdrant_service.create_collection_if_not_exists()
        qdrant_service.create_payload_indices()

    # Run ingestion
    ingester = ContentIngester(base_url=args.base_url)
    total_chunks = await ingester.ingest_directory(docs_dir, batch_size=args.batch_size)

    # Print summary
    logger.info("=" * 60)
    logger.info("Ingestion Summary")
    logger.info("=" * 60)
    logger.info(f"Source: {docs_dir}")
    logger.info(f"Total chunks ingested: {total_chunks}")

    try:
        info = qdrant_service.get_collection_info()
        logger.info(f"Collection vectors count: {info['vectors_count']}")
        logger.info(f"Collection status: {info['status']}")
    except Exception as e:
        logger.warning(f"Could not get collection info: {e}")

    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
