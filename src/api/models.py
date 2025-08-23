# src/api/models.py
"""
Pydantic Data Models for API Request and Response Schemas.

This module defines the data structures used for validating incoming API
requests and for serializing outgoing API responses. Using Pydantic models ensures
data integrity and provides automatic, clear error messages for invalid inputs.
These models also power the automatic generation of OpenAPI (Swagger) documentation.
"""

from typing import List, Literal
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """
    Represents the schema for an incoming question to the `/ask` endpoint.
    """
    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="The user's question about the university.",
        examples=["What are the admission deadlines for the computer science program?"]
    )
    language: Literal["Polish", "English"] = Field(
        "Polish",  # Default value
        description="The language for the generated answer."
    )


class Source(BaseModel):
    """
    Represents a single source document used to generate an answer.
    """
    url: str = Field(
        ...,
        description="The full URL of the source page.",
        examples=["https://example-university.com/admissions/deadlines"]
    )
    title: str = Field(
        ...,
        description="The title of the source page.",
        examples=["Admission Deadlines - Example University"]
    )


class AskResponse(BaseModel):
    """
    Represents the structured response sent back by the `/ask` endpoint.
    """
    answer: str = Field(
        ...,
        description="The generated answer to the user's question.",
        examples=["The admission deadline is July 15th."]
    )
    sources: List[Source] = Field(
        ...,
        description="A list of source documents that were used to formulate the answer."
    )
