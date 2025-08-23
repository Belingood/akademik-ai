# src/api/endpoints.py
"""
API Endpoints for the RAG (Retrieval-Augmented Generation) service.

This module defines the FastAPI routes that expose the functionality of the
AkademikAI application to external clients.
"""

from fastapi import APIRouter, Depends, HTTPException

from src.api.models import AskRequest, AskResponse
from src.core.dependencies import get_rag_pipeline
from src.core.rag_pipeline import RAGPipeline

# Create a new router object to organize endpoints.
# This router will be included in the main FastAPI application.
router = APIRouter()


@router.post(
    "/ask",
    response_model=AskResponse,
    tags=["RAG"],
    summary="Ask a question about the university",
    description=(
        "Accepts a user's question, processes it through the RAG pipeline, "
        "and returns a generated answer along with the source documents used."
    )
)
def ask(
    request: AskRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline)
) -> AskResponse:
    """
    Handles a user's question by performing the following steps:
    1.  Receives the question via a POST request.
    2.  Uses FastAPI's dependency injection to get a ready-to-use RAGPipeline instance.
    3.  Calls the pipeline's `answer` method to get a result.
    4.  Handles potential errors during processing.
    5.  Returns a structured `AskResponse` containing the answer and sources.

    Args:
        request (AskRequest): The incoming request body with the user's question.
        pipeline (RAGPipeline): The dependency-injected RAG pipeline instance.

    Returns:
        AskResponse: The structured response containing the answer and source URLs.
    """
    try:
        result = pipeline.answer(
            question=request.question,
            language=request.language
        )
        return AskResponse(**result)
    except Exception as e:
        # Basic error handling for any unexpected issues in the pipeline.
        # This prevents the server from crashing and provides a clear error message.
        # In a production environment, you would log this exception.
        # logger.error(f"An error occurred in the RAG pipeline: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occurred while processing the request: {e}"
        )
