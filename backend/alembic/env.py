import asyncio
from logging.config import fileConfig
import sys
import os

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# ------------------------------------------------------------------------
# 1. Add the project root to sys.path so we can import 'app'
# ------------------------------------------------------------------------
sys.path.append(os.getcwd())

# ------------------------------------------------------------------------
# 2. Import your Base, Config, and Models
#    (Models must be imported for metadata to be detected!)
# ------------------------------------------------------------------------
from app.core.config import Settings
from app.models.base import Base
# Strictly import all models here so Alembic detects them
from app.models import customer, transaction 

# ------------------------------------------------------------------------
# 3. Load Config
# ------------------------------------------------------------------------
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ------------------------------------------------------------------------
# 4. Set Target Metadata
# ------------------------------------------------------------------------
target_metadata = Base.metadata

# ------------------------------------------------------------------------
# 5. Dynamic DB URL from Settings (Single Source of Truth)
# ------------------------------------------------------------------------
settings = Settings()
# Overwrite the sqlalchemy.url in the alembic config with our app config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())