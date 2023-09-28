from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.conf import config
from src.log import logger

# Create Database Connection:
Base = declarative_base()

# Init Database engine:
engine = create_engine(config.DATABASE_URL)
Base.metadata.create_all(engine)

connection = engine.connect()
logger.info(f"Connected to database {config.DATABASE_URL}")

# Create Database Session:
try:
    db: Session = sessionmaker(bind=engine)()
except:
    logger.exception("Failed to create DBSession")
    raise
