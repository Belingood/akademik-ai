# config.py
"""
Centralized configuration management for the AkademikAI project.

This module uses pydantic-settings to manage application settings, allowing for
type-hinted, validated configurations that can be loaded from an environment
variable file (.env).
"""

from pathlib import Path
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Define the absolute path to the project's root directory. This ensures that all
# file paths constructed from here are robust and independent of the current
# working directory from which scripts are run.
BASE_DIR = Path(__file__).parent.resolve()


class Settings(BaseSettings):
    """
    Defines and validates the main application settings.

    Attributes are automatically loaded from a .env file. Pydantic ensures that
    required variables are present and have the correct data type.
    """
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # --- Indexing & Data Source ---
    DATA_PATH: Path = BASE_DIR / "data" / "content.jsonl"
    DB_PATH: Path = BASE_DIR / "vector_db"
    EMBEDDING_MODEL_NAME: str = 'intfloat/multilingual-e5-large'

    # --- Text Splitting Parameters ---
    CHUNK_SIZE: int = 1500
    CHUNK_OVERLAP: int = 200

    # --- LLM & API Configuration ---
    OPENAI_API_KEY: Optional[str] = None

    @field_validator("OPENAI_API_KEY")
    @classmethod
    def validate_api_key_is_present(cls, v: Optional[str]) -> str:
        """
        Validate that the OPENAI_API_KEY is loaded from the environment and is not empty.
        """
        if v is None or not v.strip():
            raise ValueError(
                "OPENAI_API_KEY is not set in the .env file or environment variables. "
                "It is required to run the application."
            )
        return v


# Create a single, globally accessible instance of the settings.
# Import this instance into other modules to access configuration values.
# Example: `from config import settings`
settings = Settings()
