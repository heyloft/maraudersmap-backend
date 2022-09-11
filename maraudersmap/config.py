from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_CONNECTION_STRING: str | None = None

    class Config:
        fields = {
            "DATABASE_CONNECTION_STRING": {
                "env": ["DATABASE_CONNECTION_STRING", "DATABASE_URL"]
            }
        }
