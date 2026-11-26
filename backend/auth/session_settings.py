import os
from functools import lru_cache
from pathlib import Path
from typing import Final

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field

ENV_FILE_PATH: Final = Path(__file__).resolve().parent.parent / ".env"
SECRET_KEY_VARIABLE: Final = "SESSION_SECRET_KEY"
OWNER_EMAIL_VARIABLE: Final = "OWNER_EMAIL"
MIN_SECRET_KEY_LENGTH: Final = 32


class SessionSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    secret_key: str = Field(min_length=MIN_SECRET_KEY_LENGTH)
    owner_email: str = Field(min_length=1)


@lru_cache
def get_session_settings() -> SessionSettings:
    """
    Reads the login settings from the backend's .env file.
    Stops the app with a clear error if one is missing or too short.
    """
    load_dotenv(ENV_FILE_PATH)
    return SessionSettings(
        secret_key=os.environ.get(SECRET_KEY_VARIABLE, ""),
        owner_email=os.environ.get(OWNER_EMAIL_VARIABLE, "").strip().lower(),
    )