from sqlalchemy import create_engine
from app.core.config import Settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

settings = Settings()
engine = create_engine(settings.postgres_url,echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


