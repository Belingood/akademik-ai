# src/main.py
"""
Main application file for the AkademikAI FastAPI service.

This module initializes the FastAPI application, loads environment variables,
sets up API metadata, and includes the API routers from other modules.
This file serves as the entry point for the Uvicorn ASGI server.
"""

from dotenv import load_dotenv

# Load environment variables from a .env file into the application's
# environment. This must be done before importing any module that
# relies on environment variables (like 'config' or 'dependencies').
load_dotenv()

from fastapi import FastAPI
from src.api import endpoints

# --- Application Metadata ---
# This information will be displayed in the OpenAPI (Swagger) documentation.
app_metadata = {
    "title": "AkademikAI API",
    "version": "1.0.0",
    "description": (
        "A Retrieval-Augmented Generation (RAG) API to answer questions "
        "about a university based on its official website content."
    ),
    "contact": {
        "name": "Your Name or Project Name",
        "url": "http://your.github.repo.url.com",
    },
    "license_info": {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
}

# --- FastAPI App Initialization ---
app = FastAPI(**app_metadata)

# --- Include API Routers ---
# Include the router from the endpoints module. All routes defined in that
# router will be prefixed with /api/v1.
app.include_router(endpoints.router, prefix="/api/v1")


# --- Root Endpoint / Health Check ---
@app.get("/", tags=["Health Check"], summary="Check the API's operational status.")
async def root():
    """
    A simple health check endpoint.

    Returns a confirmation message if the API is running, which is useful for
    liveness probes in deployment environments.
    """
    return {"message": "AkademikAI API is running!"}
