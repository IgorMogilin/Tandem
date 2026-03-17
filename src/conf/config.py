from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DB_USER: str = Field(description="Пользователь", default="postgres", examples=["postgres"])
    DB_PASS: str = Field(description="Пароль", default="postgres", examples=["postgres"])
    DB_HOST: str = Field(description="Адрес хоста", default="localhost", examples=["localhost"])
    DB_PORT: int = Field(description="Номер порта", default=5432, examples=[5432])
    DB_NAME: str = Field(description="имя базы данных", default="tandem_db", examples=["tandem_db"])

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def URL_ALEMBIC(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
