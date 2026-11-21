from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///assistant.db"

# Creating an engine
sync_engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
    pool_size=5,
    max_overflow=10
)
# sync session factory
session_factory = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=sync_engine)
