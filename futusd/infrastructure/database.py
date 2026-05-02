from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from futusd.config import PostgresConfig

def new_session_maker(psql_config: PostgresConfig) -> async_sessionmaker[AsyncSession]:
    database_url = 'postgresql+asyncpg://{login}:{password}@{host}:{port}/{database}'.format(
        login=psql_config.login,
        password=psql_config.password,
        host=psql_config.host,
        port=psql_config.port,
        database=psql_config.database,
    )

    engine = create_async_engine(
        database_url,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "command_timeout": 5,
        },
    )
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)