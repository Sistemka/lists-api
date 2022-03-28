from pathlib import Path

import dotenv
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    PORT: int = 8010
    IS_DEBUG: bool = False

    TITLE: str = "Lists Api"
    VERSION: str = "0.1.0"

    DATABASE_PORT: int
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_USER: str

    @property
    def pg_conn(self) -> dict:
        return {
            "host": self.DATABASE_HOST,
            "port": self.DATABASE_PORT,
            "user": self.DATABASE_USER,
            "password": self.DATABASE_PASSWORD,
            "database": self.DATABASE_NAME,
        }

    class Config:
        env_file = Path(BASE_DIR, ".env")
        dotenv.load_dotenv(env_file)


settings = Settings()

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": settings.pg_conn,
        }
    },
    "apps": {
        "models": {
            "models": [
                *[
                    f"db.models.{model_file.stem}"
                    for model_file in Path(BASE_DIR, "db", "models").glob("*.py")
                ],
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "UTC",
}
