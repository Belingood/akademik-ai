# src/data_processing/loader.py
"""
Data Loading and Preparation Utilities.

This module provides functions for loading raw data from source files
and transforming it into a standardized format suitable for the RAG pipeline.
"""

import json
import logging
from pathlib import Path
from typing import List, Optional
from itertools import islice

from langchain_core.documents import Document

# Initialize a logger for this module to provide feedback on its operations.
logger = logging.getLogger(__name__)


def load_and_prepare_documents(
    file_path: Path,
    start: int = 0,
    stop: Optional[int] = None
) -> List[Document]:
    """
    Loads documents from a .jsonl file within a specified line range.

    This function reads each JSON object from a line, enriches the text content
    with title and H1 metadata for better semantic context, and converts it into
    a LangChain `Document` object. It uses `itertools.islice` for efficient,
    memory-friendly reading of large files.

    Args:
        file_path (Path): The path to the .jsonl file.
        start (int): The starting line number to read from (inclusive). Defaults to 0.
        stop (Optional[int]): The ending line number to read to (exclusive).
                              If None, reads to the end of the file. Defaults to None.

    Returns:
        List[Document]: A list of prepared `Document` objects.
    """
    documents: List[Document] = []
    logger.info(f"Loading documents from '{file_path}' [lines {start}-{stop or 'end'}]...")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Use islice to efficiently slice the file iterator without
            # loading the entire file into memory.
            file_iterator = islice(f, start, stop)

            for i, line in enumerate(file_iterator, start=start):
                try:
                    data = json.loads(line)

                    # Enrich content for better context in embeddings
                    enriched_content = (
                        f"Page Title: {data.get('title', 'N/A')}\n"
                        f"H1 Header: {data.get('h1', 'N/A')}\n\n"
                        f"{data.get('text', '')}"
                    )

                    metadata = {
                        "source": data.get('url', ''),
                        "title": data.get('title', 'No Title'),
                        "content_hash": data.get('content_hash', ''),
                    }

                    doc = Document(page_content=enriched_content, metadata=metadata)
                    documents.append(doc)

                except json.JSONDecodeError:
                    # Log a warning for corrupted lines but continue processing.
                    logger.warning(
                        f"Skipping malformed JSON line {i + 1} in '{file_path}'."
                    )
                    continue
                except (TypeError, KeyError) as e:
                    # Handle cases where the JSON is valid but missing expected keys.
                    logger.warning(
                        f"Skipping line {i + 1} due to missing data in '{file_path}': {e}"
                    )
                    continue

    except FileNotFoundError:
        logger.error(f"Data file not found at path: {file_path}")
        # Return an empty list or re-raise the exception depending on desired behavior.
        # Returning an empty list is safer for the indexing script.
        return []

    logger.info(f"Successfully loaded and prepared {len(documents)} documents.")
    return documents
