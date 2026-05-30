from os import environ as env
from pydantic import BaseModel, Field

class PostgresConfig(BaseModel):
    host: str
    port: int
    login: str
    password: str
    database: str

class RedisConfig(BaseModel):
    host: str
    port: int

class GroqConfig(BaseModel):
    api_key: str
    model: str

class Config(BaseModel):
    postgres: PostgresConfig = Field(
        default_factory=lambda: PostgresConfig(
            host=env["POSTGRES_HOST"],
            port=int(env["POSTGRES_PORT"]),
            login=env["POSTGRES_USER"],
            password=env["POSTGRES_PASSWORD"],
            database=env["POSTGRES_DB"],
        )
    )

    redis: RedisConfig = Field(
        default_factory=lambda: RedisConfig(
            host=env["REDIS_HOST"],
            port=int(env["REDIS_PORT"])
        )
    )

    groq: GroqConfig = Field(
        default_factory=lambda: GroqConfig(
            api_key=env["GROQ_API_KEY"],
            model=env["GROQ_MODEL"]
        )
    )
