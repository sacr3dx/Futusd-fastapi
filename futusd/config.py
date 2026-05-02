from os import environ as env
from pydantic import BaseModel, Field

class PostgresConfig(BaseModel):
    host: str
    port: int
    login: str
    password: str
    database: str

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