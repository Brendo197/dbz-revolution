from logging.config import fileConfig
from alembic import context
import os
import sys

sys.path.append(os.getcwd())

from database.db import engine, DB_PATH
from database.models import Base
from database.models import *

config = context.config

config.set_main_option(
    "sqlalchemy.url",
    f"sqlite:///{DB_PATH}"
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_online():
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()