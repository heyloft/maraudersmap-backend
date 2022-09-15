from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    DATABASE_CONNECTION_STRING: str | None = None

    @validator("DATABASE_CONNECTION_STRING", pre=True, always=True)
    def replace_deprecated_db_dialect(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.replace(
            # SQLAlchemy 1.4 removed deprecated 'postgres://',
            # but fly.io still uses it...
            "postgres://",
            "postgresql://",
            1,
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        fields = {
            "DATABASE_CONNECTION_STRING": {
                # fly.io injects DATABASE_URL, so we define it as an alias
                "env": ["DATABASE_CONNECTION_STRING", "DATABASE_URL"]
            }
        }
