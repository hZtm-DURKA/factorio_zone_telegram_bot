from dotenv import find_dotenv

from pydantic import BaseModel

from pydantic_settings import BaseSettings, SettingsConfigDict


class Telegram(BaseModel):
    token: str


class FactorioZone(BaseModel):
    token: str
    base_url: str
    ws_url: str


class Database(BaseModel):
    driver: str = "sqlite"
    database: str = "database.db"
    username: str | None = None
    password: str | None = None
    host: str | None = None
    port: int | None = None
    echo: bool = False

    @property
    def dsn(self) -> str:
        return f"{self.driver}:///{self.database}"


class Config(BaseSettings):
    admin_token: str
    telegram: Telegram
    factorio_zone: FactorioZone
    database: Database = Database()

    model_config = SettingsConfigDict(
        env_file=(
            find_dotenv(filename=".env.default"),
            find_dotenv(filename=".env"),
        ),
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        extra="ignore",
    )


CONFIG = Config()
