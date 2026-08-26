import os
from sqlalchemy import create_engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/pricing_db"
)


engine = create_engine(
    DATABASE_URL
)
