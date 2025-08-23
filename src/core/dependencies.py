# src/core/dependencies.py
"""
Dependency Injection Providers for Core Application Components.

This module defines functions that create and cache singleton instances of heavy
objects like machine learning models and database connections. These functions are
designed to be used with FastAPI's dependency injection system.

The `@lru_cache(maxsize=1)` decorator ensures that each function is executed only
once, and its result is cached and reused across subsequent requests, preventing
costly re-initializations.
"""

import logging
from functools import lru_cache

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStore

from config import settings
from src.core.rag_pipeline import RAGPipeline

# It's a good practice to have a logger in this module to report
# on the initialization of these heavy components.
logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Creates and returns a singleton instance of the embedding model.
    The model is loaded into memory only on the first call to this function.

    Returns:
        HuggingFaceEmbeddings: The initialized sentence-transformer embedding model.
    """
    logger.info(f"Loading embedding model '{settings.EMBEDDING_MODEL_NAME}'...")
    model = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    logger.info("Embedding model loaded successfully.")
    return model


@lru_cache(maxsize=1)
def get_vector_store() -> VectorStore:
    """
    Creates and returns a singleton instance of the vector store client.
    It checks for the database's existence before attempting to load it.

    Returns:
        VectorStore: An instance of the Chroma vector store.

    Raises:
        FileNotFoundError: If the vector database directory does not exist.
    """
    logger.info(f"Connecting to vector store at: {settings.DB_PATH}")
    if not settings.DB_PATH.exists():
        error_msg = (
            f"Vector database not found at '{settings.DB_PATH}'. "
            "Please run the indexing script first: `python scripts/build_index.py`"
        )
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    embedding_model = get_embedding_model()
    vector_store = Chroma(
        persist_directory=str(settings.DB_PATH),
        embedding_function=embedding_model
    )
    logger.info("Vector store connected successfully.")
    return vector_store


@lru_cache(maxsize=1)
def get_llm() -> BaseChatModel:
    """
    Creates and returns a singleton instance of the Language Model (LLM).
    The API key is automatically read from the OPENAI_API_KEY environment variable.

    Returns:
        BaseChatModel: An instance of the ChatOpenAI model.
    """
    logger.info("Initializing LLM (gpt-4o)...")
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
    logger.info("LLM initialized successfully.")
    return llm


@lru_cache(maxsize=1)
def get_rag_pipeline() -> RAGPipeline:
    """
    Assembles the complete RAG pipeline from its components.
    This is the primary dependency used by the API endpoints.

    Returns:
        RAGPipeline: The fully assembled, ready-to-use RAG pipeline.
    """
    logger.info("Assembling the RAG pipeline...")
    llm = get_llm()
    vector_store = get_vector_store()
    pipeline = RAGPipeline(llm=llm, vector_store=vector_store)
    logger.info("RAG pipeline assembled successfully.")
    return pipeline
