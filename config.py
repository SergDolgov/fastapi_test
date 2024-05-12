import os 
from pathlib import Path
import tomllib
from typing import Literal
import logging

from pydantic import AnyHttpUrl, EmailStr

from starlette.config import Config

log = logging.getLogger(__name__)
logging.getLogger('passlib').setLevel(logging.ERROR)

config = Config(".env")

PROJECT_DIR = Path(__file__).parent
with open(os.path.join(PROJECT_DIR , "pyproject.toml"), "rb") as f:
    PYPROJECT_CONTENT = tomllib.load(f)["tool"]["poetry"]

# PROJECT NAME, VERSION AND DESCRIPTION
PROJECT_NAME = PYPROJECT_CONTENT["name"]
VERSION = PYPROJECT_CONTENT["version"]
DESCRIPTION = PYPROJECT_CONTENT["description"]

# CORE SETTINGS
SECRET_KEY = config("SECRET_KEY")
ENVIRONMENT: Literal["DEV", "PYTEST", "STG", "PRD"] = config("ENVIRONMENT", default = "DEV") 
SECURITY_BCRYPT_ROUNDS = config("SECURITY_BCRYPT_ROUNDS", default = 12)
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default = 11520)  # 8 days
REFRESH_TOKEN_EXPIRE_MINUTES = config("REFRESH_TOKEN_EXPIRE_MINUTES", default = 40320)  # 28 days
BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = config("BACKEND_CORS_ORIGINS", default = ["http://localhost:3000"])
ALLOWED_HOSTS: list[str] = config("ALLOWED_HOSTS", default = ["localhost", "127.0.0.1"])

JWT_SECRET=config("JWT_SECRET")
JWT_EXPIRES=config("JWT_EXPIRES")
JWT_ALGORITHM=config("JWT_ALGORITHM")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
UNIT_TEST = config("UNIT_TEST", cast=bool, default=False)
DEPLOYMENT_ENV: str = config("DEPLOYMENT_ENV", default="local")


# STATIC DIR
DEFAULT_STATIC_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), os.path.join("static", "dispatch", "dist")
)
STATIC_DIR = config("STATIC_DIR", default=DEFAULT_STATIC_DIR)

# DATABASE TYPE
DATABASE_TYPE=config("DATABASE_TYPE") 

# SQLLITE DATABASE
SQLLITE_DATABASE_URI = config("SQLLITE_DATABASE_URI")

# POSTGRESQL DEFAULT DATABASE
DEFAULT_DATABASE_HOSTNAME = config("DEFAULT_DATABASE_HOSTNAME")
DEFAULT_DATABASE_USER = config("DEFAULT_DATABASE_USER")
DEFAULT_DATABASE_PASSWORD = config("DEFAULT_DATABASE_PASSWORD")
DEFAULT_DATABASE_PORT = config("DEFAULT_DATABASE_PORT")
DEFAULT_DATABASE_DB = config("DEFAULT_DATABASE_DB")
DEFAULT_SQLALCHEMY_DATABASE_URI = f"postgresql+asyncpg://{DEFAULT_DATABASE_USER}:{DEFAULT_DATABASE_PASSWORD}@{DEFAULT_DATABASE_HOSTNAME}:{DEFAULT_DATABASE_PORT}/{DEFAULT_DATABASE_DB}"


# FIRST SUPERUSER
FIRST_SUPERUSER_EMAIL = config("FIRST_SUPERUSER_EMAIL")
FIRST_SUPERUSER_PASSWORD = config("FIRST_SUPERUSER_PASSWORD")

# LOGGING
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
# logging.basicConfig(handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL)
# logger.configure(
#     handlers=[{"sink": sys.stdout, "level": LOGGING_LEVEL, "format": Formatter().format}]
# )

ALEMBIC_CORE_REVISION_PATH = config(
    "ALEMBIC_CORE_REVISION_PATH",
    default=f"{os.path.dirname(os.path.realpath(__file__))}/database/revisions/core",
)
ALEMBIC_TENANT_REVISION_PATH = config(
    "ALEMBIC_TENANT_REVISION_PATH",
    default=f"{os.path.dirname(os.path.realpath(__file__))}/database/revisions/tenant",
)
ALEMBIC_INI_PATH = config(
    "ALEMBIC_INI_PATH",
    default=f"{os.path.dirname(os.path.realpath(__file__))}/alembic.ini",
)
ALEMBIC_MULTI_TENANT_MIGRATION_PATH = config(
    "ALEMBIC_MULTI_TENANT_MIGRATION_PATH",
    default=f"{os.path.dirname(os.path.realpath(__file__))}/database/revisions/multi-tenant-migration.sql",
)

